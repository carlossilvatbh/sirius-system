from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from .models import UBO


class UBOModelTest(TestCase):
    """
    Testes unitários para o modelo UBO (Ultimate Beneficial Owner)
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.ubo_data = {
            'nome_completo': 'João Silva Santos',
            'data_nascimento': date(1980, 1, 15),
            'nacionalidade': 'BR',
            'tin': 'CPF12345678901'
        }
    
    def test_create_ubo_valid(self):
        """Testa criação de UBO com dados válidos"""
        ubo = UBO.objects.create(**self.ubo_data)
        self.assertEqual(ubo.nome_completo, 'João Silva Santos')
        self.assertEqual(ubo.nacionalidade, 'BR')
        self.assertEqual(ubo.tin, 'CPF12345678901')
        self.assertTrue(ubo.ativo)
        self.assertIsNotNone(ubo.created_at)
        self.assertIsNotNone(ubo.updated_at)
    
    def test_ubo_str_representation(self):
        """Testa representação string do UBO"""
        ubo = UBO.objects.create(**self.ubo_data)
        expected = f"{self.ubo_data['nome_completo']} ({self.ubo_data['tin']})"
        self.assertEqual(str(ubo), expected)
    
    def test_ubo_tin_validation_valid(self):
        """Testa validação de TIN com valores válidos"""
        valid_tins = [
            'CPF12345678901',
            'SSN123456789',
            'TIN-123-456-789',
            'ABC123DEF456',
            '12345'
        ]
        
        for tin in valid_tins:
            with self.subTest(tin=tin):
                self.ubo_data['tin'] = tin
                ubo = UBO(**self.ubo_data)
                try:
                    ubo.full_clean()
                except ValidationError:
                    self.fail(f"TIN válido '{tin}' foi rejeitado")
    
    def test_ubo_tin_validation_invalid(self):
        """Testa validação de TIN com valores inválidos"""
        invalid_tins = [
            'invalid@tin',  # Contém caractere especial inválido
            'abc',          # Muito curto
            'a' * 25,       # Muito longo
            'TIN WITH SPACES',  # Contém espaços
            '',             # Vazio
        ]
        
        for tin in invalid_tins:
            with self.subTest(tin=tin):
                self.ubo_data['tin'] = tin
                ubo = UBO(**self.ubo_data)
                with self.assertRaises(ValidationError):
                    ubo.full_clean()
    
    def test_ubo_nacionalidade_choices(self):
        """Testa se todas as nacionalidades definidas são válidas"""
        nacionalidades_validas = [choice[0] for choice in UBO.NACIONALIDADES]
        
        for nacionalidade in nacionalidades_validas:
            with self.subTest(nacionalidade=nacionalidade):
                self.ubo_data['nacionalidade'] = nacionalidade
                ubo = UBO.objects.create(**self.ubo_data)
                self.assertEqual(ubo.nacionalidade, nacionalidade)
    
    def test_ubo_campos_opcionais(self):
        """Testa criação de UBO apenas com campos obrigatórios"""
        ubo = UBO.objects.create(**self.ubo_data)
        self.assertEqual(ubo.endereco_residencia_fiscal, '')
        self.assertEqual(ubo.telefone, '')
        self.assertEqual(ubo.email, '')
        self.assertEqual(ubo.observacoes, '')
    
    def test_ubo_campos_opcionais_preenchidos(self):
        """Testa criação de UBO com todos os campos preenchidos"""
        dados_completos = {
            **self.ubo_data,
            'endereco_residencia_fiscal': 'Rua das Flores, 123, São Paulo, SP, Brasil',
            'telefone': '+55 11 99999-9999',
            'email': 'joao.silva@email.com',
            'observacoes': 'Cliente VIP com estruturas complexas'
        }
        
        ubo = UBO.objects.create(**dados_completos)
        self.assertEqual(ubo.endereco_residencia_fiscal, dados_completos['endereco_residencia_fiscal'])
        self.assertEqual(ubo.telefone, dados_completos['telefone'])
        self.assertEqual(ubo.email, dados_completos['email'])
        self.assertEqual(ubo.observacoes, dados_completos['observacoes'])
    
    def test_ubo_email_validation(self):
        """Testa validação de email"""
        # Email válido
        self.ubo_data['email'] = 'teste@email.com'
        ubo = UBO(**self.ubo_data)
        ubo.full_clean()  # Não deve gerar erro
        
        # Email inválido
        self.ubo_data['email'] = 'email_invalido'
        ubo = UBO(**self.ubo_data)
        with self.assertRaises(ValidationError):
            ubo.full_clean()
    
    def test_ubo_ordering(self):
        """Testa ordenação dos UBOs por nome_completo"""
        ubo1 = UBO.objects.create(
            nome_completo='Carlos Silva',
            data_nascimento=date(1975, 5, 10),
            nacionalidade='BR',
            tin='TIN001'
        )
        ubo2 = UBO.objects.create(
            nome_completo='Ana Santos',
            data_nascimento=date(1980, 3, 15),
            nacionalidade='US',
            tin='TIN002'
        )
        ubo3 = UBO.objects.create(
            nome_completo='Bruno Costa',
            data_nascimento=date(1985, 8, 20),
            nacionalidade='CH',
            tin='TIN003'
        )
        
        ubos = list(UBO.objects.all())
        self.assertEqual(ubos[0], ubo2)  # Ana Santos
        self.assertEqual(ubos[1], ubo3)  # Bruno Costa
        self.assertEqual(ubos[2], ubo1)  # Carlos Silva
    
    def test_ubo_get_nacionalidade_display(self):
        """Testa método get_nacionalidade_display"""
        ubo = UBO.objects.create(**self.ubo_data)
        self.assertEqual(ubo.get_nacionalidade_display(), 'Brasil')
        
        ubo.nacionalidade = 'US'
        ubo.save()
        self.assertEqual(ubo.get_nacionalidade_display(), 'Estados Unidos')
    
    def test_ubo_methods_placeholder(self):
        """Testa métodos auxiliares (implementação placeholder)"""
        ubo = UBO.objects.create(**self.ubo_data)
        
        # Métodos retornam listas vazias por enquanto (serão implementados nas próximas fases)
        self.assertEqual(ubo.get_products_associados(), [])
        self.assertEqual(ubo.get_structures_associadas(), [])
    
    def test_ubo_ativo_default(self):
        """Testa valor padrão do campo ativo"""
        ubo = UBO.objects.create(**self.ubo_data)
        self.assertTrue(ubo.ativo)
    
    def test_ubo_meta_verbose_names(self):
        """Testa nomes verbose do modelo"""
        self.assertEqual(UBO._meta.verbose_name, "Ultimate Beneficial Owner")
        self.assertEqual(UBO._meta.verbose_name_plural, "Ultimate Beneficial Owners")

