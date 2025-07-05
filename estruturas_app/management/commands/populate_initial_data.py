from django.core.management.base import BaseCommand
from estruturas_app.models import Estrutura, RegraValidacao, Template, AlertaJurisdicao


class Command(BaseCommand):
    help = 'Populate initial data for SIRIUS system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting initial data population...'))
        
        # Create legal structures
        self.create_estruturas()
        
        # Create validation rules
        self.create_regras_validacao()
        
        # Create jurisdiction alerts
        self.create_alertas_jurisdicao()
        
        # Create sample templates
        self.create_templates()
        
        self.stdout.write(self.style.SUCCESS('Initial data population completed successfully!'))

    def create_estruturas(self):
        """Create the legal structures as specified in the technical documentation."""
        
        estruturas_data = [
            {
                'nome': 'Bahamas DAO SAC',
                'tipo': 'BDAO_SAC',
                'descricao': 'Bahamas Decentralized Autonomous Organization Segregated Account Compartment. Combines characteristics of investment funds with traditional corporate structures.',
                'custo_base': 15000.00,
                'custo_manutencao': 8000.00,
                'tempo_implementacao': 45,
                'complexidade': 4,
                'impacto_tributario_eua': 'Acts as Estate Tax Blocker for US inheritance tax (40%) applicable to non-residents with US assets over $60,000. Treated as pass-through entity for IRC purposes. Taxation only on effective distributions to US beneficiaries. Subject to FATCA reporting if US persons are beneficiaries.',
                'impacto_tributario_brasil': 'May be classified as offshore investment fund by CVM. Subject to semi-annual come-cotas (15%) on presumed gains. Mandatory DCBE declaration. IOF incidence on exchange operations (0.38% to 6.38%).',
                'nivel_confidencialidade': 4,
                'protecao_patrimonial': 3,
                'impacto_privacidade': 'High level of confidentiality through Account Token segregation. Beneficial ownership registry maintained in Bahamas (not public). Subject to CRS automatic information exchange. Asset protection limited to accounting segregation.',
                'facilidade_banking': 3,
                'documentacao_necessaria': 'Corporate documents, beneficial ownership information, compliance certificates, registered agent appointment.',
                'formularios_obrigatorios_eua': 'Form 3520 (for US person beneficiaries), Form 8865 (if applicable)',
                'formularios_obrigatorios_brasil': 'DCBE (Declaration of Brazilian Capital Abroad), DIRPF'
            },
            {
                'nome': 'Wyoming DAO LLC',
                'tipo': 'WYOMING_DAO_LLC',
                'descricao': 'Wyoming Decentralized Autonomous Organization Limited Liability Company. Evolution of traditional LLCs incorporating decentralized autonomous organization characteristics.',
                'custo_base': 8000.00,
                'custo_manutencao': 3000.00,
                'tempo_implementacao': 21,
                'complexidade': 2,
                'impacto_tributario_eua': 'Disregarded Entity if single member (complete tax transparency). Partnership if multiple members (pass-through taxation). ECI taxation only if effectively connected income to US. 30% withholding tax on passive US source income (reducible by treaties).',
                'impacto_tributario_brasil': 'Subject to CFC (Controlled Foreign Corporation) rules. Taxation 15% to 25% on profits earned abroad. IRPJ/CSLL incidence on available profits.',
                'nivel_confidencialidade': 2,
                'protecao_patrimonial': 2,
                'impacto_privacidade': 'Basic information available in Wyoming Secretary of State public registry. Does not require public disclosure of members. Facilitates US bank account opening. Lower regulatory burden compared to corporations.',
                'facilidade_banking': 4,
                'documentacao_necessaria': 'Articles of Organization, Operating Agreement, registered agent appointment, EIN application.',
                'formularios_obrigatorios_eua': 'Form 1065 (if partnership), Form 5472 (if foreign-owned)',
                'formularios_obrigatorios_brasil': 'DIRPF, CFC reporting'
            },
            {
                'nome': 'BTS Vault',
                'tipo': 'BTS_VAULT',
                'descricao': 'Basket Token Standard protocol based on ERC-721 (Ethereum) functioning as wallet-as-a-token with financial arrangement characteristics and technological shielding through blockchain.',
                'custo_base': 25000.00,
                'custo_manutencao': 5000.00,
                'tempo_implementacao': 60,
                'complexidade': 5,
                'impacto_tributario_eua': 'Treated as property for tax purposes by IRS. Capital gains taxation on disposition. Staking rewards taxed as ordinary income. Reporting via Form 8949, Schedule D.',
                'impacto_tributario_brasil': 'Classified as digital asset/cryptocurrency by RFB. 15% taxation on capital gains (operations above R$ 35,000/month). Day trade: 20% on gains. Declaration in DIRPF with specific crypto attachment.',
                'nivel_confidencialidade': 5,
                'protecao_patrimonial': 5,
                'impacto_privacidade': 'Pseudonymous transactions (traceable but pseudonymous). Subject to KYC/AML regulations of exchanges. Compliance varies by jurisdiction of use.',
                'facilidade_banking': 2,
                'documentacao_necessaria': 'Smart contract deployment, token specifications, compliance documentation, exchange listings.',
                'formularios_obrigatorios_eua': 'Form 8949, Schedule D, FBAR (if applicable)',
                'formularios_obrigatorios_brasil': 'DIRPF with crypto attachment, monthly crypto reporting'
            },
            {
                'nome': 'Wyoming Statutory Foundation',
                'tipo': 'WYOMING_FOUNDATION',
                'descricao': 'Wyoming statutory foundation functioning as non-profit entity with specific purpose, offering advanced asset protection structure.',
                'custo_base': 35000.00,
                'custo_manutencao': 12000.00,
                'tempo_implementacao': 90,
                'complexidade': 5,
                'impacto_tributario_eua': 'Classified as Foreign Trust for tax purposes by IRS. Grantor Trust Rules applicable if US grantor. US beneficiaries taxed on distributions received. Creditor protection after 2-year period (statute of limitations).',
                'impacto_tributario_brasil': 'Classified as foreign trust or foundation. Come-cotas on presumed income. Brazilian beneficiaries taxed on distributions.',
                'nivel_confidencialidade': 5,
                'protecao_patrimonial': 5,
                'impacto_privacidade': 'High confidentiality protection. Robust asset protection against creditors. Effective tool for succession planning.',
                'facilidade_banking': 3,
                'documentacao_necessaria': 'Foundation charter, bylaws, trustee appointments, beneficial ownership documentation.',
                'formularios_obrigatorios_eua': 'Form 3520-A, Form 3520',
                'formularios_obrigatorios_brasil': 'DCBE, DIRPF, come-cotas reporting'
            },
            {
                'nome': 'Wyoming Corporation',
                'tipo': 'WYOMING_CORP',
                'descricao': 'Traditional Wyoming corporation serving as versatile corporate structure for various business purposes including tax blockers, active income structures, and nationalization vehicles.',
                'custo_base': 12000.00,
                'custo_manutencao': 4000.00,
                'tempo_implementacao': 30,
                'complexidade': 3,
                'impacto_tributario_eua': 'Corporate tax: 21% on profits (C-Corp). Double taxation: corporate + dividends. S-Election possibility for tax transparency. Wyoming has no state income tax.',
                'impacto_tributario_brasil': 'Subject to CFC rules. Nationalization: CNPJ obtainment process. Taxation: Real profit, presumed profit, or Simples (after nationalization).',
                'nivel_confidencialidade': 2,
                'protecao_patrimonial': 3,
                'impacto_privacidade': 'Standard corporate privacy protections. Public filing requirements. Beneficial ownership reporting may apply.',
                'facilidade_banking': 5,
                'documentacao_necessaria': 'Articles of Incorporation, bylaws, corporate resolutions, registered agent appointment.',
                'formularios_obrigatorios_eua': 'Form 1120 (C-Corp), Form 1120S (S-Corp)',
                'formularios_obrigatorios_brasil': 'CNPJ registration (if nationalized), CFC reporting'
            },
            {
                'nome': 'Nacionalização (CNPJ Brasil)',
                'tipo': 'NATIONALIZATION',
                'descricao': 'Process of obtaining Brazilian CNPJ for foreign corporations, allowing local operation with benefits of international structure.',
                'custo_base': 5000.00,
                'custo_manutencao': 8000.00,
                'tempo_implementacao': 60,
                'complexidade': 3,
                'impacto_tributario_eua': 'No direct US tax impact. Maintains foreign corporation status for US purposes.',
                'impacto_tributario_brasil': 'Tax regime: Real profit, presumed profit, or Simples Nacional. IRPJ: 15% + 10% additional (real profit). CSLL: 9% (general) or 15% (financial institutions). PIS/COFINS: Cumulative or non-cumulative.',
                'nivel_confidencialidade': 1,
                'protecao_patrimonial': 2,
                'impacto_privacidade': 'Brazilian corporate transparency requirements. Public CNPJ registry. Beneficial ownership disclosure requirements.',
                'facilidade_banking': 5,
                'documentacao_necessaria': 'Foreign corporation documents, apostilled certificates, legal representative appointment, address proof.',
                'formularios_obrigatorios_eua': 'None (maintains foreign status)',
                'formularios_obrigatorios_brasil': 'CNPJ registration, ECF, DEFIS (if applicable)'
            },
            {
                'nome': 'Fund Token as a Service',
                'tipo': 'FUND_TOKEN',
                'descricao': 'Investment fund structures using Digital Offshore framework to create personalized investment funds, offering clients the possibility to structure investment vehicles with specific characteristics.',
                'custo_base': 45000.00,
                'custo_manutencao': 15000.00,
                'tempo_implementacao': 120,
                'complexidade': 5,
                'impacto_tributario_eua': 'Follows Digital Offshore taxation structure. Additional fund management regulations may apply. PFIC rules may apply to US investors.',
                'impacto_tributario_brasil': 'Fund management regulation by CVM applicable. Investor taxation according to profile (individual/corporate, resident/non-resident). Come-cotas for offshore funds.',
                'nivel_confidencialidade': 4,
                'protecao_patrimonial': 4,
                'impacto_privacidade': 'Fund structure confidentiality. Investor privacy protections. Regulatory reporting requirements.',
                'facilidade_banking': 3,
                'documentacao_necessaria': 'Fund documentation, investment policy, regulatory compliance, custodian agreements.',
                'formularios_obrigatorios_eua': 'Fund reporting forms, PFIC elections (if applicable)',
                'formularios_obrigatorios_brasil': 'CVM fund registration, investor reporting'
            }
        ]
        
        for data in estruturas_data:
            estrutura, created = Estrutura.objects.get_or_create(
                nome=data['nome'],
                tipo=data['tipo'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created structure: {estrutura.nome}')
            else:
                self.stdout.write(f'Structure already exists: {estrutura.nome}')

    def create_regras_validacao(self):
        """Create validation rules between structures."""
        
        # Get structures for rule creation
        bdao_sac = Estrutura.objects.get(tipo='BDAO_SAC')
        wyoming_dao = Estrutura.objects.get(tipo='WYOMING_DAO_LLC')
        bts_vault = Estrutura.objects.get(tipo='BTS_VAULT')
        wyoming_foundation = Estrutura.objects.get(tipo='WYOMING_FOUNDATION')
        wyoming_corp = Estrutura.objects.get(tipo='WYOMING_CORP')
        nationalization = Estrutura.objects.get(tipo='NATIONALIZATION')
        fund_token = Estrutura.objects.get(tipo='FUND_TOKEN')
        
        regras_data = [
            {
                'estrutura_a': bdao_sac,
                'estrutura_b': wyoming_dao,
                'tipo_relacionamento': 'RECOMMENDED',
                'severidade': 'INFO',
                'descricao': 'Digital Offshore Basic combines BDAO SAC with Wyoming DAO LLC for comprehensive tax optimization.',
                'jurisdicao_aplicavel': 'US/BS'
            },
            {
                'estrutura_a': wyoming_corp,
                'estrutura_b': nationalization,
                'tipo_relacionamento': 'REQUIRED',
                'severidade': 'ERROR',
                'descricao': 'Nationalization can only be applied to Wyoming Corporations.',
                'jurisdicao_aplicavel': 'BR'
            },
            {
                'estrutura_a': bts_vault,
                'estrutura_b': wyoming_foundation,
                'tipo_relacionamento': 'SYNERGISTIC',
                'severidade': 'INFO',
                'descricao': 'BTS Vault combined with Wyoming Foundation provides maximum asset protection and privacy.',
                'jurisdicao_aplicavel': 'GLOBAL'
            },
            {
                'estrutura_a': fund_token,
                'estrutura_b': bdao_sac,
                'tipo_relacionamento': 'REQUIRED',
                'severidade': 'WARNING',
                'descricao': 'Fund Token as a Service requires Digital Offshore base structure.',
                'jurisdicao_aplicavel': 'GLOBAL'
            },
            {
                'estrutura_a': nationalization,
                'estrutura_b': bts_vault,
                'tipo_relacionamento': 'INCOMPATIBLE',
                'severidade': 'ERROR',
                'descricao': 'Nationalized entities cannot directly hold crypto assets like BTS Vault.',
                'jurisdicao_aplicavel': 'BR'
            }
        ]
        
        for data in regras_data:
            regra, created = RegraValidacao.objects.get_or_create(
                estrutura_a=data['estrutura_a'],
                estrutura_b=data['estrutura_b'],
                tipo_relacionamento=data['tipo_relacionamento'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created validation rule: {regra}')

    def create_alertas_jurisdicao(self):
        """Create jurisdiction-specific alerts."""
        
        alertas_data = [
            {
                'jurisdicao': 'US',
                'tipo_alerta': 'TAX',
                'titulo': 'FATCA Reporting Requirements',
                'descricao': 'US persons with foreign financial accounts must report under FATCA. Failure to report can result in significant penalties.',
                'prioridade': 4
            },
            {
                'jurisdicao': 'BR',
                'tipo_alerta': 'COMPLIANCE',
                'titulo': 'DCBE Declaration Deadline',
                'descricao': 'Brazilian residents must declare foreign capital by April 30th annually. Late filing incurs penalties.',
                'prioridade': 5
            },
            {
                'jurisdicao': 'US',
                'tipo_alerta': 'REPORTING',
                'titulo': 'Form 3520 Filing Requirement',
                'descricao': 'US persons receiving distributions from foreign trusts must file Form 3520. Due with tax return.',
                'prioridade': 4
            },
            {
                'jurisdicao': 'BR',
                'tipo_alerta': 'TAX',
                'titulo': 'Come-Cotas Tax on Offshore Funds',
                'descricao': 'Semi-annual taxation (15%) on presumed gains from offshore investment funds. Due on last business day of May and November.',
                'prioridade': 3
            },
            {
                'jurisdicao': 'GLOBAL',
                'tipo_alerta': 'REGULATORY',
                'titulo': 'CRS Automatic Exchange',
                'descricao': 'Common Reporting Standard requires automatic exchange of financial information between participating countries.',
                'prioridade': 3
            }
        ]
        
        for data in alertas_data:
            alerta, created = AlertaJurisdicao.objects.get_or_create(
                titulo=data['titulo'],
                jurisdicao=data['jurisdicao'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created jurisdiction alert: {alerta.titulo}')

    def create_templates(self):
        """Create sample templates for different business sectors."""
        
        # Get structures for template creation
        bdao_sac = Estrutura.objects.get(tipo='BDAO_SAC')
        wyoming_dao = Estrutura.objects.get(tipo='WYOMING_DAO_LLC')
        wyoming_corp = Estrutura.objects.get(tipo='WYOMING_CORP')
        wyoming_foundation = Estrutura.objects.get(tipo='WYOMING_FOUNDATION')
        bts_vault = Estrutura.objects.get(tipo='BTS_VAULT')
        
        templates_data = [
            {
                'nome': 'Tech Startup Basic',
                'categoria': 'TECH',
                'complexidade_template': 'BASIC',
                'descricao': 'Basic structure for technology startups seeking international tax optimization.',
                'configuracao': {
                    'elementos': [
                        {'estrutura_id': wyoming_dao.id, 'position': {'x': 100, 'y': 100}},
                        {'estrutura_id': wyoming_corp.id, 'position': {'x': 300, 'y': 100}}
                    ],
                    'conexoes': []
                },
                'custo_total': float(wyoming_dao.custo_base + wyoming_corp.custo_base),
                'tempo_total_implementacao': max(wyoming_dao.tempo_implementacao, wyoming_corp.tempo_implementacao),
                'publico_alvo': 'Technology startups, software companies, digital service providers',
                'casos_uso': 'IP protection, international expansion, tax optimization for digital services'
            },
            {
                'nome': 'Family Office Advanced',
                'categoria': 'FAMILY_OFFICE',
                'complexidade_template': 'ADVANCED',
                'descricao': 'Comprehensive asset protection and succession planning structure.',
                'configuracao': {
                    'elementos': [
                        {'estrutura_id': wyoming_foundation.id, 'position': {'x': 150, 'y': 50}},
                        {'estrutura_id': bts_vault.id, 'position': {'x': 150, 'y': 200}},
                        {'estrutura_id': bdao_sac.id, 'position': {'x': 350, 'y': 125}}
                    ],
                    'conexoes': []
                },
                'custo_total': float(wyoming_foundation.custo_base + bts_vault.custo_base + bdao_sac.custo_base),
                'tempo_total_implementacao': max(wyoming_foundation.tempo_implementacao, bts_vault.tempo_implementacao, bdao_sac.tempo_implementacao),
                'publico_alvo': 'High net worth families, family offices, wealth management',
                'casos_uso': 'Asset protection, succession planning, privacy enhancement, multi-generational wealth transfer'
            },
            {
                'nome': 'Real Estate Investment',
                'categoria': 'REAL_ESTATE',
                'complexidade_template': 'INTERMEDIATE',
                'descricao': 'Optimized structure for real estate investments and property holding.',
                'configuracao': {
                    'elementos': [
                        {'estrutura_id': wyoming_corp.id, 'position': {'x': 200, 'y': 100}},
                        {'estrutura_id': bdao_sac.id, 'position': {'x': 400, 'y': 100}}
                    ],
                    'conexoes': []
                },
                'custo_total': float(wyoming_corp.custo_base + bdao_sac.custo_base),
                'tempo_total_implementacao': max(wyoming_corp.tempo_implementacao, bdao_sac.tempo_implementacao),
                'publico_alvo': 'Real estate investors, property developers, REITs',
                'casos_uso': 'Property holding, rental income optimization, real estate development'
            }
        ]
        
        for data in templates_data:
            template, created = Template.objects.get_or_create(
                nome=data['nome'],
                categoria=data['categoria'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created template: {template.nome}')

