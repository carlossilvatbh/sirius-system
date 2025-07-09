from django.core.management.base import BaseCommand
from django.db import transaction
from corporate.models import Entity, Structure, EntityOwnership, UBO, ValidationRule
from sales.models import Partner, Contact, StructureRequest, StructureApproval
from financial_department.models import EntityPrice, IncorporationCost
from parties.models import Party, PartyRole, Passport
from decimal import Decimal
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula dados iniciais para demonstração do sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população de dados iniciais...'))
        
        try:
            with transaction.atomic():
                # 1. Criar entidades de exemplo
                self.create_sample_entities()
                
                # 2. Criar estruturas de exemplo
                self.create_sample_structures()
                
                # 3. Criar UBOs de exemplo
                self.create_sample_ubos()
                
                # 4. Criar parties de exemplo
                self.create_sample_parties()
                
                # 5. Criar partners de exemplo
                self.create_sample_partners()
                
                # 6. Criar preços de exemplo
                self.create_sample_prices()
                
                # 7. Criar relacionamentos de propriedade
                self.create_sample_ownerships()
                
                self.stdout.write(self.style.SUCCESS('População de dados concluída com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante a população: {str(e)}'))
            raise

    def create_sample_entities(self):
        """Cria entidades de exemplo"""
        self.stdout.write('Criando entidades de exemplo...')
        
        entities_data = [
            {
                'name': 'Delaware Trust Holdings',
                'entity_type': 'TRUST',
                'tax_classification': 'TRUST',
                'jurisdiction': 'US',
                'us_state': 'DE',
                'privacy_score': 3,
                'compliance_score': 90,
                'implementation_time': 30,
                'active': True,
                'complexity': 4,
                'confidentiality_level': 4,
                'asset_protection': 5,
                'banking_relation_score': 2,
                'banking_facility': 3,
            },
            {
                'name': 'Cayman Islands Fund',
                'entity_type': 'FUND',
                'tax_classification': 'FUND',
                'jurisdiction': 'KY',
                'privacy_score': 3,
                'compliance_score': 85,
                'implementation_time': 45,
                'active': True,
                'complexity': 5,
                'confidentiality_level': 5,
                'asset_protection': 4,
                'banking_relation_score': 3,
                'banking_facility': 2,
            },
            {
                'name': 'BVI International Business Company',
                'entity_type': 'IBC',
                'tax_classification': 'OFFSHORE_CORP',
                'jurisdiction': 'VG',
                'privacy_score': 3,
                'compliance_score': 80,
                'implementation_time': 21,
                'active': True,
                'complexity': 3,
                'confidentiality_level': 4,
                'asset_protection': 4,
                'banking_relation_score': 2,
                'banking_facility': 3,
            },
            {
                'name': 'Wyoming LLC Disregarded',
                'entity_type': 'LLC_DISREGARDED',
                'tax_classification': 'LLC_DISREGARDED_ENTITY',
                'jurisdiction': 'US',
                'us_state': 'WY',
                'privacy_score': 2,
                'compliance_score': 95,
                'implementation_time': 14,
                'active': True,
                'complexity': 2,
                'confidentiality_level': 3,
                'asset_protection': 3,
                'banking_relation_score': 1,
                'banking_facility': 4,
            },
            {
                'name': 'Nevada Corporation',
                'entity_type': 'CORP',
                'tax_classification': 'US_CORP',
                'jurisdiction': 'US',
                'us_state': 'NV',
                'privacy_score': 2,
                'compliance_score': 90,
                'implementation_time': 10,
                'active': True,
                'complexity': 1,
                'confidentiality_level': 2,
                'asset_protection': 2,
                'banking_relation_score': 1,
                'banking_facility': 5,
            },
        ]
        
        for entity_data in entities_data:
            entity, created = Entity.objects.get_or_create(
                name=entity_data['name'],
                defaults=entity_data
            )
            if created:
                self.stdout.write(f'  - Criada entidade: {entity.name}')

    def create_sample_structures(self):
        """Cria estruturas de exemplo"""
        self.stdout.write('Criando estruturas de exemplo...')
        
        structures_data = [
            {
                'name': 'Estrutura Patrimonial Familiar',
                'description': 'Estrutura completa para proteção patrimonial familiar',
                'status': 'ACTIVE',
            },
            {
                'name': 'Estrutura de Investimento Internacional',
                'description': 'Estrutura para investimentos em múltiplas jurisdições',
                'status': 'ACTIVE',
            },
            {
                'name': 'Estrutura de Planejamento Sucessório',
                'description': 'Estrutura focada em planejamento sucessório e gestão de ativos',
                'status': 'ACTIVE',
            },
        ]
        
        for structure_data in structures_data:
            structure, created = Structure.objects.get_or_create(
                name=structure_data['name'],
                defaults=structure_data
            )
            if created:
                self.stdout.write(f'  - Criada estrutura: {structure.name}')

    def create_sample_ubos(self):
        """Cria UBOs de exemplo"""
        self.stdout.write('Criando UBOs de exemplo...')
        
        ubos_data = [
            {
                'nome': 'João Silva Santos',
                'nome_completo': 'João Silva Santos',
                'tipo_pessoa': 'FISICA',
                'nacionalidade': 'BR',
                'data_nascimento': date(1975, 5, 15),
                'documento_identidade': '123.456.789-01',
                'tipo_documento': 'CPF',
                'email': 'joao.silva@email.com',
                'telefone': '+55 11 99999-1234',
                'endereco': 'Rua das Flores, 123 - São Paulo, SP',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'pais': 'Brasil',
                'cep': '01234-567',
                'tin': '123.456.789-01',
                'ativo': True,
            },
            {
                'nome': 'Maria Oliveira Costa',
                'nome_completo': 'Maria Oliveira Costa',
                'tipo_pessoa': 'FISICA',
                'nacionalidade': 'BR',
                'data_nascimento': date(1980, 8, 22),
                'documento_identidade': '987.654.321-09',
                'tipo_documento': 'CPF',
                'email': 'maria.oliveira@email.com',
                'telefone': '+55 11 88888-5678',
                'endereco': 'Av. Paulista, 456 - São Paulo, SP',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'pais': 'Brasil',
                'cep': '01310-100',
                'tin': '987.654.321-09',
                'ativo': True,
            },
            {
                'nome': 'Robert Johnson',
                'nome_completo': 'Robert Johnson',
                'tipo_pessoa': 'FISICA',
                'nacionalidade': 'US',
                'data_nascimento': date(1970, 12, 10),
                'documento_identidade': '123-45-6789',
                'tipo_documento': 'SSN',
                'email': 'robert.johnson@email.com',
                'telefone': '+1 555 123-4567',
                'endereco': '123 Main St, New York, NY',
                'cidade': 'New York',
                'estado': 'NY',
                'pais': 'United States',
                'cep': '10001',
                'tin': '123-45-6789',
                'ativo': True,
            },
        ]
        
        for ubo_data in ubos_data:
            ubo, created = UBO.objects.get_or_create(
                nome=ubo_data['nome'],
                defaults=ubo_data
            )
            if created:
                self.stdout.write(f'  - Criado UBO: {ubo.nome}')

    def create_sample_parties(self):
        """Cria parties de exemplo"""
        self.stdout.write('Criando parties de exemplo...')
        
        parties_data = [
            {
                'name': 'Carlos Eduardo Mendes',
                'person_type': 'NATURAL_PERSON',
                'nationality': 'BR',
                'birth_date': date(1985, 3, 18),
                'tax_identification_number': '111.222.333-44',
                'email': 'carlos.mendes@email.com',
                'phone': '+55 11 77777-9999',
                'address': 'Rua Augusta, 789',
                'city': 'São Paulo',
                'state': 'SP',
                'country': 'Brasil',
                'postal_code': '01305-100',
                'active': True,
            },
            {
                'name': 'Ana Paula Rodrigues',
                'person_type': 'NATURAL_PERSON',
                'nationality': 'BR',
                'birth_date': date(1988, 7, 25),
                'tax_identification_number': '555.666.777-88',
                'email': 'ana.rodrigues@email.com',
                'phone': '+55 11 66666-1111',
                'address': 'Rua Oscar Freire, 321',
                'city': 'São Paulo',
                'state': 'SP',
                'country': 'Brasil',
                'postal_code': '01426-001',
                'active': True,
            },
        ]
        
        for party_data in parties_data:
            party, created = Party.objects.get_or_create(
                name=party_data['name'],
                defaults=party_data
            )
            if created:
                self.stdout.write(f'  - Criado party: {party.name}')

    def create_sample_partners(self):
        """Cria partners de exemplo"""
        self.stdout.write('Criando partners de exemplo...')
        
        # Primeiro criar parties para os partners
        partner_parties_data = [
            {
                'name': 'Escritório Silva & Associados',
                'person_type': 'JURIDICAL_PERSON',
                'nationality': 'BR',
                'email': 'contato@silvaassociados.com.br',
                'phone': '+55 11 3333-4444',
                'address': 'Av. Faria Lima, 1000',
                'city': 'São Paulo',
                'state': 'SP',
                'country': 'Brasil',
                'postal_code': '01452-000',
                'is_partner': True,
                'active': True,
            },
            {
                'name': 'International Trust Services',
                'person_type': 'JURIDICAL_PERSON',
                'nationality': 'US',
                'email': 'info@intltrustservices.com',
                'phone': '+1 302 555-0123',
                'address': '123 Corporate Blvd',
                'city': 'Wilmington',
                'state': 'DE',
                'country': 'United States',
                'postal_code': '19801',
                'is_partner': True,
                'active': True,
            },
            {
                'name': 'Offshore Management Ltd',
                'person_type': 'JURIDICAL_PERSON',
                'nationality': 'VG',
                'email': 'contact@offshoremanagement.vg',
                'phone': '+1 284 555-0456',
                'address': 'Waterfront Plaza',
                'city': 'Road Town',
                'state': 'Tortola',
                'country': 'British Virgin Islands',
                'postal_code': 'VG1110',
                'is_partner': True,
                'active': True,
            },
        ]
        
        # Criar as parties primeiro
        for party_data in partner_parties_data:
            party, created = Party.objects.get_or_create(
                name=party_data['name'],
                defaults=party_data
            )
            if created:
                self.stdout.write(f'  - Criado party para partner: {party.name}')
            
            # Criar o partner usando a party
            partner, created = Partner.objects.get_or_create(
                party=party,
                defaults={
                    'company_name': party_data['name'],
                    'address': f"{party_data['address']}, {party_data['city']}, {party_data['state']}, {party_data['country']}",
                    'partnership_status': 'ACTIVE',
                }
            )
            if created:
                self.stdout.write(f'  - Criado partner: {partner.company_name}')

    def create_sample_prices(self):
        """Cria preços de exemplo"""
        self.stdout.write('Criando preços de exemplo...')
        
        entities = Entity.objects.all()
        
        for entity in entities:
            # Criar preço de entidade
            entity_price, created = EntityPrice.objects.get_or_create(
                entity=entity,
                defaults={
                    'base_currency': 'USD',
                    'markup_type': 'PERCENTAGE',
                    'markup_value': Decimal(str(random.randint(10, 50))),
                }
            )
            
            if created:
                # Criar custos de incorporação
                IncorporationCost.objects.get_or_create(
                    entity_price=entity_price,
                    name='Legal Fee',
                    defaults={
                        'cost_type': 'LEGAL_FEE',
                        'value': Decimal(str(random.randint(1000, 5000))),
                    }
                )
                
                IncorporationCost.objects.get_or_create(
                    entity_price=entity_price,
                    name='Service Provider Fee',
                    defaults={
                        'cost_type': 'SERVICE_PROVIDER',
                        'value': Decimal(str(random.randint(500, 2000))),
                    }
                )
        
        self.stdout.write(f'  - Criados preços para {entities.count()} entidades')

    def create_sample_ownerships(self):
        """Cria relacionamentos de propriedade de exemplo"""
        self.stdout.write('Criando relacionamentos de propriedade...')
        
        entities = list(Entity.objects.all())
        structures = list(Structure.objects.all())
        parties = list(Party.objects.filter(person_type='NATURAL_PERSON'))
        
        if entities and structures and parties:
            # Criar alguns relacionamentos de propriedade
            for i in range(min(3, len(entities), len(structures), len(parties))):
                EntityOwnership.objects.get_or_create(
                    structure=structures[i % len(structures)],
                    owner_ubo=parties[i % len(parties)],
                    owned_entity=entities[i],
                    defaults={
                        'ownership_percentage': Decimal(str(random.randint(25, 100))),
                        'owned_shares': random.randint(100, 1000),
                        'share_value_usd': Decimal(str(random.randint(10, 100))),
                        'corporate_name': f"Corporate Entity {i+1}",
                        'hash_number': f"HASH{i+1:03d}",
                    }
                )
            
            self.stdout.write('  - Criados relacionamentos de propriedade')
        else:
            self.stdout.write('  - Pulando relacionamentos: dados insuficientes')
