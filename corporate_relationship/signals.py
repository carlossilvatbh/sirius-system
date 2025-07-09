import logging
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from sales.models import PersonalizedProduct
from .models import RelationshipStructure, WebhookLog
from sales.models import Partner  # Client foi migrado para Partner no sales

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PersonalizedProduct)
def handle_personalized_product_approval(sender, instance, created, **kwargs):
    """
    Signal para tratar aprovação de PersonalizedProduct.
    
    Ao mudar status para APPROVED:
    1. Cria RelationshipStructure para cada Structure
    2. Dispara webhook
    3. Clona serviços padrão (TODO: implementar quando definidos)
    """
    # Verifica se é uma mudança para status APPROVED
    if not hasattr(instance, '_previous_status'):
        # Na primeira criação, salvar o status atual para próximas comparações
        instance._previous_status = instance.status
        return
    
    previous_status = getattr(instance, '_previous_status', None)
    current_status = instance.status
    
    # Só processa se mudou PARA APPROVED
    if previous_status != 'APPROVED' and current_status == 'APPROVED':
        logger.info(f"Processing approval for PersonalizedProduct {instance.id}")
        
        try:
            # 1. Criar/recuperar RelationshipStructure para cada Structure
            partner = _get_or_create_partner_for_product(instance)
            structures_ids = []
            
            # FIXME: confirmar como obter structures do PersonalizedProduct
            # Assumindo que existe um relacionamento structures ou similar
            if hasattr(instance, 'structures'):
                structures = instance.structures.all()
            elif hasattr(instance, 'base_structure') and instance.base_structure:
                structures = [instance.base_structure]
            else:
                # Tentar através de base_product se existir
                structures = []
                if hasattr(instance, 'base_product') and instance.base_product:
                    # Implementar lógica para obter structures do product
                    pass
            
            for structure in structures:
                relationship, created = RelationshipStructure.objects.get_or_create(
                    structure=structure,
                    # client=partner,  # Comentado pois RelationshipStructure pode não ter campo client
                    defaults={'status': 'ACTIVE'}
                )
                structures_ids.append(structure.id)
                
                if created:
                    logger.info(f"Created RelationshipStructure for {structure.nome} - {partner.party.name}")
                
                # TODO: Clonar serviços padrão da estrutura
                # _clone_default_services_for_structure(structure, relationship)
            
            # 2. Disparar webhook
            _send_approval_webhook(instance, structures_ids, partner)
            
        except Exception as e:
            logger.error(f"Error processing PersonalizedProduct approval: {str(e)}")
            # Continua a execução mesmo com erro para não quebrar o save
    
    # Atualizar status anterior para próxima comparação
    instance._previous_status = current_status


def _get_or_create_partner_for_product(product):
    """
    Obtém ou cria um Partner baseado no PersonalizedProduct.
    
    FIXME: confirmar regra de negócio para identificar/criar partner
    """
    # Por enquanto, usar informações básicas do produto
    # Em um cenário real, isso viria de UBO ou campos específicos
    
    partner_name = f"Partner for Product {product.id}"
    
    # Tentar extrair informações de UBOs se existirem
    if hasattr(product, 'ubos') and product.ubos.exists():
        first_ubo = product.ubos.first()
        if first_ubo and first_ubo.nome:
            partner_name = f"Company of {first_ubo.nome}"
    
    # Criar Party primeiro (necessário para Partner)
    from parties.models import Party
    party, created = Party.objects.get_or_create(
        name=partner_name,
        defaults={'person_type': 'LEGAL_ENTITY'}
    )
    
    partner, created = Partner.objects.get_or_create(
        party=party,
        defaults={}
    )
    
    if created:
        logger.info(f"Created new partner: {partner_name}")
    
    return partner


def _send_approval_webhook(product, structures_ids, partner):
    """
    Envia webhook de aprovação de produto.
    """
    payload = {
        "event": "personalized_product_approved",
        "product_id": product.id,
        "structures": structures_ids,
        "partner_id": partner.id,
        "approved_at": timezone.now().isoformat(),
    }
    
    webhook_url = getattr(settings, 'RELATIONSHIP_WEBHOOK_URL', None)
    if not webhook_url:
        logger.warning("RELATIONSHIP_WEBHOOK_URL not configured")
        return
    
    # Criar log de webhook
    webhook_log = WebhookLog.objects.create(
        event_type="personalized_product_approved",
        payload=payload,
        url=webhook_url,
        status='PENDING'
    )
    
    try:
        timeout = getattr(settings, 'WEBHOOK_TIMEOUT', 10)
        response = requests.post(
            webhook_url, 
            json=payload, 
            timeout=timeout,
            headers={'Content-Type': 'application/json'}
        )
        
        # Atualizar log com resposta
        webhook_log.status = 'SUCCESS' if response.status_code < 400 else 'FAILED'
        webhook_log.response_status_code = response.status_code
        webhook_log.response_body = response.text[:1000]  # Limitar tamanho
        webhook_log.save()
        
        if response.status_code >= 400:
            logger.warning(f"Webhook returned status {response.status_code}")
        else:
            logger.info(f"Webhook sent successfully for product {product.id}")
            
    except requests.exceptions.RequestException as e:
        webhook_log.status = 'FAILED'
        webhook_log.error_message = str(e)[:500]  # Limitar tamanho
        webhook_log.save()
        
        logger.error(f"Failed to send webhook: {str(e)}")


# TODO: Implementar clonagem de serviços padrão
def _clone_default_services_for_structure(structure, relationship):
    """
    Clona serviços padrão associados a uma estrutura.
    
    FIXME: confirmar regra de negócio para serviços padrão
    """
    pass
