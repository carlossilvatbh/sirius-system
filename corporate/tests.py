from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from corporate.models import Structure, UBO, StructureOwnership
from corporate_relationship.models import Client, Service
from sales.models import PersonalizedProduct
from djmoney.money import Money


class StructureModelTest(TestCase):
    def setUp(self):
        self.structure_data = {
            'nome': 'Test LLC',
            'tipo': 'LLC_DISREGARDED',
            'tax_classification': 'LLC_DISREGARDED_ENTITY',
            'descricao': 'Test structure for unit testing',
            'jurisdicao': 'US',
            'estado_us': 'DE',
            'custo_base': 1000.00,
            'custo_manutencao': 500.00,
        }

    def test_structure_creation(self):
        structure = Structure.objects.create(**self.structure_data)
        self.assertEqual(structure.nome, 'Test LLC')
        self.assertEqual(structure.tipo, 'LLC_DISREGARDED')
        self.assertEqual(structure.get_custo_total_primeiro_ano(), 1500.00)

    def test_jurisdiction_validation(self):
        # Test that BR state cannot be set for US jurisdiction
        with self.assertRaises(ValidationError):
            structure = Structure(**self.structure_data)
            structure.estado_br = 'SP'
            structure.full_clean()


class ClientModelTest(TestCase):
    def test_client_creation(self):
        client = Client.objects.create(
            company_name='Test Client Inc.',
            address='123 Test Street, Test City, TC 12345',
        )
        self.assertEqual(client.company_name, 'Test Client Inc.')


class ServiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(
            company_name='Test Client Inc.',
            address='123 Test Street, Test City, TC 12345',
        )

    def test_service_creation_with_money(self):
        service = Service.objects.create(
            name='Corporate Setup',
            description='Setup service for corporation',
            service_price=Money(1000, 'USD'),
            regulator_fee=Money(500, 'USD'),
            executor=self.user,
            counterparty_name='Delaware Secretary of State',
        )
        self.assertEqual(service.name, 'Corporate Setup')
        self.assertEqual(service.service_price.amount, 1000)
        self.assertEqual(service.service_price.currency.code, 'USD')


class PersonalizedProductTest(TestCase):
    def setUp(self):
        self.structure = Structure.objects.create(
            nome='Test Structure',
            tipo='CORP',
            descricao='Test',
            jurisdicao='US',
            custo_base=1000.00,
            custo_manutencao=500.00,
        )

    def test_personalized_product_approval(self):
        product = PersonalizedProduct.objects.create(
            nome='Test Product',
            base_structure=self.structure,
            descricao='Test product description',
            status='DRAFT',
        )
        
        # Test status change to approved
        product.status = 'APPROVED'
        product.save()
        
        self.assertEqual(product.status, 'APPROVED')


class JurisdictionAlertTest(TestCase):
    def setUp(self):
        self.structure = Structure.objects.create(
            nome='Test Structure for Alert',
            tipo='CORP',
            descricao='Test structure for alert testing',
            jurisdicao='US',
            custo_base=1000.00,
            custo_manutencao=500.00,
        )

    def test_single_deadline_alert_creation(self):
        from datetime import date, timedelta
        alert = JurisdictionAlert.objects.create(
            titulo='Annual Filing',
            descricao='Annual corporate filing requirement',
            jurisdicao='US',
            tipo_alerta='FILING',
            deadline_type='SINGLE',
            single_deadline=date.today() + timedelta(days=90),
        )
        alert.estruturas_aplicaveis.add(self.structure)
        
        self.assertEqual(alert.titulo, 'Annual Filing')
        self.assertEqual(alert.deadline_type, 'SINGLE')
        self.assertTrue(alert.estruturas_aplicaveis.filter(pk=self.structure.pk).exists())

    def test_recurring_deadline_alert_creation(self):
        alert = JurisdictionAlert.objects.create(
            titulo='Quarterly Report',
            descricao='Quarterly tax reporting requirement',
            jurisdicao='US',
            tipo_alerta='TAX',
            deadline_type='RECURRING',
            recurrence_pattern='QUARTERLY',
        )
        
        self.assertEqual(alert.recurrence_pattern, 'QUARTERLY')
        next_deadline = alert.calculate_next_deadline()
        self.assertIsNotNone(next_deadline)

    def test_alert_validation_errors(self):
        from django.core.exceptions import ValidationError
        
        # Test single deadline without date
        with self.assertRaises(ValidationError):
            alert = JurisdictionAlert(
                titulo='Invalid Alert',
                descricao='Missing deadline',
                jurisdicao='US',
                tipo_alerta='TAX',
                deadline_type='SINGLE',
            )
            alert.full_clean()

        # Test recurring deadline without pattern
        with self.assertRaises(ValidationError):
            alert = JurisdictionAlert(
                titulo='Invalid Recurring Alert',
                descricao='Missing recurrence pattern',
                jurisdicao='US',
                tipo_alerta='TAX',
                deadline_type='RECURRING',
            )
            alert.full_clean()
