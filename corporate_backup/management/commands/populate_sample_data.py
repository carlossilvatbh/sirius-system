from django.core.management.base import BaseCommand
from django.db import transaction
from corporate.models import TaxClassification, Structure, UBO
from sales.models import Product, ProductHierarchy, PersonalizedProduct, PersonalizedProductUBO
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula dados iniciais para demonstração do sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando população de dados iniciais...'))
        
        try:
            with transaction.atomic():
                # 1. Criar algumas estruturas de exemplo
                self.create_sample_structures()
                
                # 2. Criar alguns UBOs de exemplo
                self.create_sample_ubos()
                
                # 3. Criar alguns produtos de exemplo
                self.create_sample_products()
                
                # 4. Criar produtos personalizados
                self.create_sample_personalized_products()
                
                self.stdout.write(self.style.SUCCESS('População de dados concluída com sucesso!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro durante a população: {str(e)}'))
            raise

    def create_sample_structures(self):
        """Cria estruturas de exemplo"""
        self.stdout.write('Criando estruturas de exemplo...')
        
        # Trust
        trust_tax = TaxClassification.objects.get(name='TRUST')
        trust_struct, created = Structure.objects.get_or_create(
            nome='Delaware Trust',
            defaults={
                'descricao': 'Trust estabelecido em Delaware para proteção de ativos',
                'jurisdicao': 'US',
                'estado_us': 'DE',
                'custo_base': Decimal('5000.00'),
                'custo_manutencao': Decimal('2000.00'),
                'privacidade_score': 85,
                'compliance_score': 90,
                'tempo_implementacao': 30,
                'documentos_necessarios': 'Identificação dos beneficiários, documentos de trust',
                'ativo': True,
            }
        )
        if created:
            trust_struct.tax_classifications.add(trust_tax)
            self.stdout.write('  Created: Delaware Trust')
        
        # LLC
        llc_tax = TaxClassification.objects.get(name='LLC_DISREGARDED_ENTITY')
        llc_struct, created = Structure.objects.get_or_create(
            nome='Wyoming LLC',
            defaults={
                'descricao': 'LLC em Wyoming com máxima privacidade',
                'jurisdicao': 'US',
                'estado_us': 'WY',
                'custo_base': Decimal('2500.00'),
                'custo_manutencao': Decimal('500.00'),
                'privacidade_score': 95,
                'compliance_score': 80,
                'tempo_implementacao': 15,
                'documentos_necessarios': 'Articles of Organization, Operating Agreement',
                'ativo': True,
            }
        )
        if created:
            llc_struct.tax_classifications.add(llc_tax)
            self.stdout.write('  Created: Wyoming LLC')
        
        # Offshore Corp
        offshore_tax = TaxClassification.objects.get(name='OFFSHORE_CORP')
        offshore_struct, created = Structure.objects.get_or_create(
            nome='BVI IBC',
            defaults={
                'descricao': 'International Business Company nas Ilhas Virgens Britânicas',
                'jurisdicao': 'VG',
                'custo_base': Decimal('3500.00'),
                'custo_manutencao': Decimal('1200.00'),
                'privacidade_score': 90,
                'compliance_score': 75,
                'tempo_implementacao': 20,
                'documentos_necessarios': 'Memorandum e Articles of Association',
                'ativo': True,
            }
        )
        if created:
            offshore_struct.tax_classifications.add(offshore_tax)
            self.stdout.write('  Created: BVI IBC')

    def create_sample_ubos(self):
        """Cria UBOs de exemplo"""
        self.stdout.write('Criando UBOs de exemplo...')
        
        ubos_data = [
            {
                'nome': 'John Smith',
                'tipo_pessoa': 'FISICA',
                'email': 'john.smith@email.com',
                'telefone': '+1-555-0123',
                'endereco': '123 Main St, Suite 100',
                'cidade': 'Miami',
                'estado': 'Florida',
                'pais': 'United States',
                'cep': '33101',
                'documento_identidade': '123456789',
                'tipo_documento': 'US Passport',
                'nacionalidade': 'American',
            },
            {
                'nome': 'Maria Silva',
                'tipo_pessoa': 'FISICA',
                'email': 'maria.silva@email.com',
                'telefone': '+55-11-98765-4321',
                'endereco': 'Rua das Flores, 456',
                'cidade': 'São Paulo',
                'estado': 'São Paulo',
                'pais': 'Brazil',
                'cep': '01234-567',
                'documento_identidade': '123.456.789-00',
                'tipo_documento': 'CPF',
                'nacionalidade': 'Brazilian',
            },
            {
                'nome': 'Global Holdings Ltd',
                'tipo_pessoa': 'JURIDICA',
                'email': 'contact@globalholdings.com',
                'telefone': '+44-20-1234-5678',
                'endereco': '100 London Bridge St',
                'cidade': 'London',
                'estado': 'England',
                'pais': 'United Kingdom',
                'cep': 'SE1 9SG',
                'documento_identidade': '12345678',
                'tipo_documento': 'Company Registration',
                'nacionalidade': 'British',
            }
        ]
        
        for ubo_data in ubos_data:
            ubo, created = UBO.objects.get_or_create(
                nome=ubo_data['nome'],
                defaults=ubo_data
            )
            if created:
                self.stdout.write(f'  Created: {ubo_data["nome"]}')

    def create_sample_products(self):
        """Cria produtos de exemplo"""
        self.stdout.write('Criando produtos de exemplo...')
        
        # Produto 1: Asset Protection Suite
        trust_struct = Structure.objects.get(nome='Delaware Trust')
        llc_struct = Structure.objects.get(nome='Wyoming LLC')
        
        product1, created = Product.objects.get_or_create(
            nome='Asset Protection Suite',
            defaults={
                'commercial_name': 'SIRIUS Asset Protection Suite',
                'complexidade_template': 'ADVANCED',
                'descricao': 'Estrutura completa de proteção de ativos com Trust e LLC',
                'master_agreement_url': 'https://example.com/agreements/asset-protection',
                'custo_automatico': True,
                'tempo_total_implementacao': 45,
                'publico_alvo': 'High net worth individuals',
                'casos_uso': 'Proteção de ativos, planejamento sucessório, otimização fiscal',
                'ativo': True,
            }
        )
        
        if created:
            # Adicionar estruturas ao produto
            ProductHierarchy.objects.create(
                product=product1,
                structure=trust_struct,
                order=1,
                notes='Trust principal para proteção de ativos'
            )
            ProductHierarchy.objects.create(
                product=product1,
                structure=llc_struct,
                order=2,
                notes='LLC para operações comerciais'
            )
            self.stdout.write('  Created: Asset Protection Suite')
        
        # Produto 2: International Business Structure
        offshore_struct = Structure.objects.get(nome='BVI IBC')
        
        product2, created = Product.objects.get_or_create(
            nome='International Business Structure',
            defaults={
                'commercial_name': 'SIRIUS International Business Structure',
                'complexidade_template': 'INTERMEDIATE',
                'descricao': 'Estrutura internacional para negócios offshore',
                'master_agreement_url': 'https://example.com/agreements/international-business',
                'custo_automatico': True,
                'tempo_total_implementacao': 30,
                'publico_alvo': 'International businesses, crypto investors',
                'casos_uso': 'Negócios internacionais, investimentos offshore, criptomoedas',
                'ativo': True,
            }
        )
        
        if created:
            ProductHierarchy.objects.create(
                product=product2,
                structure=offshore_struct,
                order=1,
                notes='Estrutura principal para negócios internacionais'
            )
            self.stdout.write('  Created: International Business Structure')

    def create_sample_personalized_products(self):
        """Cria produtos personalizados de exemplo"""
        self.stdout.write('Criando produtos personalizados de exemplo...')
        
        # Buscar dados necessários
        product = Product.objects.get(nome='Asset Protection Suite')
        john_smith = UBO.objects.get(nome='John Smith')
        maria_silva = UBO.objects.get(nome='Maria Silva')
        
        # Produto personalizado 1
        pp1, created = PersonalizedProduct.objects.get_or_create(
            nome='Smith Family Trust Structure',
            defaults={
                'descricao': 'Estrutura personalizada para a família Smith',
                'status': 'ACTIVE',
                'base_product': product,
                'version_number': 1,
                'configuracao_personalizada': {
                    'family_name': 'Smith',
                    'trust_purpose': 'Asset Protection and Estate Planning',
                    'jurisdiction_preference': 'Delaware'
                },
                'observacoes': 'Estrutura otimizada para proteção de ativos familiares',
                'ativo': True,
            }
        )
        
        if created:
            # Adicionar UBOs com percentuais
            PersonalizedProductUBO.objects.create(
                personalized_product=pp1,
                ubo=john_smith,
                percentage=Decimal('60.00')
            )
            PersonalizedProductUBO.objects.create(
                personalized_product=pp1,
                ubo=maria_silva,
                percentage=Decimal('40.00')
            )
            self.stdout.write('  Created: Smith Family Trust Structure')
        
        # Produto personalizado 2 - baseado em estrutura única
        trust_struct = Structure.objects.get(nome='Delaware Trust')
        global_holdings = UBO.objects.get(nome='Global Holdings Ltd')
        
        pp2, created = PersonalizedProduct.objects.get_or_create(
            nome='Global Holdings Trust',
            defaults={
                'descricao': 'Trust personalizado para Global Holdings Ltd',
                'status': 'DRAFT',
                'base_structure': trust_struct,
                'version_number': 1,
                'custo_personalizado': Decimal('8000.00'),
                'configuracao_personalizada': {
                    'corporate_trustee': True,
                    'investment_focus': 'International Markets',
                    'reporting_requirements': 'Quarterly'
                },
                'observacoes': 'Trust corporativo com foco em investimentos internacionais',
                'ativo': True,
            }
        )
        
        if created:
            PersonalizedProductUBO.objects.create(
                personalized_product=pp2,
                ubo=global_holdings,
                percentage=Decimal('100.00')
            )
            self.stdout.write('  Created: Global Holdings Trust')
