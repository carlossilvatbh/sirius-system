from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from .models import UBO, Successor, Product, PersonalizedProduct, PersonalizedProductUBO, Service, ServiceActivity, AlertaJurisdicao


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




class SuccessorModelTest(TestCase):
    """
    Testes unitários para o modelo Successor
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar UBOs para testes
        self.ubo_proprietario = UBO.objects.create(
            nome_completo='Proprietário Teste',
            data_nascimento=date(1970, 1, 1),
            nacionalidade='BR',
            tin='PROP123456'
        )
        self.ubo_sucessor1 = UBO.objects.create(
            nome_completo='Sucessor 1',
            data_nascimento=date(1990, 1, 1),
            nacionalidade='BR',
            tin='SUCC123456'
        )
        self.ubo_sucessor2 = UBO.objects.create(
            nome_completo='Sucessor 2',
            data_nascimento=date(1995, 1, 1),
            nacionalidade='US',
            tin='SUCC789012'
        )
        
        self.successor_data = {
            'ubo_proprietario': self.ubo_proprietario,
            'ubo_sucessor': self.ubo_sucessor1,
            'percentual': 60.00
        }
    
    def test_create_successor_valid(self):
        """Testa criação de Successor com dados válidos"""
        successor = Successor.objects.create(**self.successor_data)
        self.assertEqual(successor.ubo_proprietario, self.ubo_proprietario)
        self.assertEqual(successor.ubo_sucessor, self.ubo_sucessor1)
        self.assertEqual(successor.percentual, 60.00)
        self.assertTrue(successor.ativo)
        self.assertFalse(successor.efetivado)
        self.assertIsNotNone(successor.created_at)
        self.assertIsNotNone(successor.updated_at)
    
    def test_successor_str_representation(self):
        """Testa representação string do Successor"""
        successor = Successor.objects.create(**self.successor_data)
        expected = f"{self.ubo_proprietario.nome_completo} → {self.ubo_sucessor1.nome_completo} (60.0%)"
        self.assertEqual(str(successor), expected)
    
    def test_self_succession_prevention(self):
        """Testa prevenção de auto-sucessão"""
        successor = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_proprietario,  # Mesmo UBO
            percentual=100.00
        )
        with self.assertRaises(ValidationError) as context:
            successor.full_clean()
        
        self.assertIn("UBO não pode ser sucessor de si mesmo", str(context.exception))
    
    def test_percentual_sum_validation_valid(self):
        """Testa validação de soma de percentuais válida"""
        # Criar primeiro sucessor com 60%
        successor1 = Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=60.00
        )
        
        # Criar segundo sucessor com 40% (total = 100%)
        successor2 = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor2,
            percentual=40.00
        )
        successor2.full_clean()  # Não deve gerar erro
        successor2.save()
        
        # Verificar que ambos foram salvos
        self.assertEqual(Successor.objects.filter(ubo_proprietario=self.ubo_proprietario).count(), 2)
    
    def test_percentual_sum_validation_invalid(self):
        """Testa validação de soma de percentuais inválida"""
        # Criar primeiro sucessor com 60%
        successor1 = Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=60.00
        )
        
        # Tentar criar segundo sucessor que excederia 100%
        successor2 = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor2,
            percentual=50.00  # 60 + 50 = 110% > 100%
        )
        
        with self.assertRaises(ValidationError) as context:
            successor2.full_clean()
        
        self.assertIn("Soma dos percentuais excede 100%", str(context.exception))
        self.assertIn("Disponível: 40.00%", str(context.exception))
    
    def test_percentual_validation_range(self):
        """Testa validação de range do percentual"""
        # Percentual muito baixo
        successor_low = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=0.00
        )
        with self.assertRaises(ValidationError):
            successor_low.full_clean()
        
        # Percentual muito alto
        successor_high = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=100.01
        )
        with self.assertRaises(ValidationError):
            successor_high.full_clean()
        
        # Percentual válido máximo
        successor_max = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=100.00
        )
        successor_max.full_clean()  # Não deve gerar erro
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together"""
        # Criar primeiro sucessor
        successor1 = Successor.objects.create(**self.successor_data)
        
        # Tentar criar segundo sucessor com mesma combinação
        with self.assertRaises(Exception):  # IntegrityError no banco
            Successor.objects.create(**self.successor_data)
    
    def test_validar_percentuais_completos_method(self):
        """Testa método validar_percentuais_completos"""
        # Sem sucessores - deve retornar False
        self.assertFalse(Successor.validar_percentuais_completos(self.ubo_proprietario))
        
        # Com sucessores que somam 100%
        Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=60.00
        )
        Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor2,
            percentual=40.00
        )
        
        self.assertTrue(Successor.validar_percentuais_completos(self.ubo_proprietario))
        
        # Com sucessores que não somam 100%
        Successor.objects.filter(ubo_proprietario=self.ubo_proprietario).delete()
        Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=50.00
        )
        
        self.assertFalse(Successor.validar_percentuais_completos(self.ubo_proprietario))
    
    def test_get_percentual_disponivel_method(self):
        """Testa método get_percentual_disponivel"""
        # Criar sucessor com 60%
        successor1 = Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=60.00
        )
        
        # Criar novo sucessor (não salvo ainda)
        successor2 = Successor(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor2,
            percentual=0.00
        )
        
        # Deve retornar 40% disponível
        self.assertEqual(successor2.get_percentual_disponivel(), 40.00)
        
        # Para o sucessor existente, deve considerar apenas outros sucessores
        self.assertEqual(successor1.get_percentual_disponivel(), 100.00)
    
    def test_successor_ordering(self):
        """Testa ordenação dos Successors por data_definicao"""
        # Criar sucessores em momentos diferentes
        successor1 = Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor1,
            percentual=60.00
        )
        
        # Simular criação posterior
        from django.utils import timezone
        import time
        time.sleep(0.01)  # Pequena pausa para garantir timestamps diferentes
        
        successor2 = Successor.objects.create(
            ubo_proprietario=self.ubo_proprietario,
            ubo_sucessor=self.ubo_sucessor2,
            percentual=40.00
        )
        
        successors = list(Successor.objects.all())
        # Deve estar ordenado por -data_definicao (mais recente primeiro)
        self.assertEqual(successors[0], successor2)
        self.assertEqual(successors[1], successor1)
    
    def test_successor_status_fields(self):
        """Testa campos de status do Successor"""
        successor = Successor.objects.create(**self.successor_data)
        
        # Valores padrão
        self.assertTrue(successor.ativo)
        self.assertFalse(successor.efetivado)
        self.assertIsNone(successor.data_efetivacao_real)
        
        # Alterar status
        successor.efetivado = True
        successor.data_efetivacao_real = timezone.now()
        successor.save()
        
        successor.refresh_from_db()
        self.assertTrue(successor.efetivado)
        self.assertIsNotNone(successor.data_efetivacao_real)
    
    def test_successor_optional_fields(self):
        """Testa campos opcionais do Successor"""
        successor_data_complete = {
            **self.successor_data,
            'data_efetivacao': date(2025, 12, 31),
            'condicoes': 'Sucessão condicionada à maioridade do sucessor'
        }
        
        successor = Successor.objects.create(**successor_data_complete)
        self.assertEqual(successor.data_efetivacao, date(2025, 12, 31))
        self.assertEqual(successor.condicoes, 'Sucessão condicionada à maioridade do sucessor')
    
    def test_successor_meta_verbose_names(self):
        """Testa nomes verbose do modelo"""
        self.assertEqual(Successor._meta.verbose_name, "Successor")
        self.assertEqual(Successor._meta.verbose_name_plural, "Successors")



class ProductModelTest(TestCase):
    """
    Testes unitários para o modelo Product
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.product_data = {
            'nome': 'Produto Teste',
            'commercial_name': 'Test Product Commercial',
            'categoria': 'TECH',
            'complexidade_template': 'INTERMEDIATE',
            'descricao': 'Descrição detalhada do produto de teste',
            'master_agreement_url': 'https://example.com/master-agreement.pdf',
            'configuracao': {'elementos': [{'estrutura_id': 1}, {'estrutura_id': 2}]},
            'tempo_total_implementacao': 30,
            'custo_manual': 5000.00
        }
    
    def test_create_product_valid(self):
        """Testa criação de Product com dados válidos"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.nome, 'Produto Teste')
        self.assertEqual(product.commercial_name, 'Test Product Commercial')
        self.assertEqual(product.categoria, 'TECH')
        self.assertTrue(product.custo_automatico)  # Valor padrão
        self.assertTrue(product.ativo)  # Valor padrão
        self.assertEqual(product.uso_count, 0)  # Valor padrão
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)
    
    def test_product_str_representation(self):
        """Testa representação string do Product"""
        product = Product.objects.create(**self.product_data)
        expected = f"{self.product_data['commercial_name']} ({self.product_data['nome']})"
        self.assertEqual(str(product), expected)
    
    def test_product_custo_automatico_default(self):
        """Testa valor padrão do campo custo_automatico"""
        product = Product.objects.create(**self.product_data)
        self.assertTrue(product.custo_automatico)
    
    def test_product_custo_manual_mode(self):
        """Testa modo de custo manual"""
        product_data = {
            **self.product_data,
            'custo_automatico': False,
            'custo_manual': 7500.00
        }
        product = Product.objects.create(**product_data)
        self.assertFalse(product.custo_automatico)
        self.assertEqual(product.custo_manual, 7500.00)
        self.assertEqual(product.get_custo_total_primeiro_ano(), 7500.00)
    
    def test_product_custo_automatico_mode(self):
        """Testa modo de custo automático"""
        product = Product.objects.create(**self.product_data)
        self.assertTrue(product.custo_automatico)
        # Por enquanto retorna 0 (será implementado na Fase 4)
        self.assertEqual(product.get_custo_total_calculado(), 0)
        self.assertEqual(product.get_custo_total_primeiro_ano(), 0)
    
    def test_product_categorias_choices(self):
        """Testa se todas as categorias definidas são válidas"""
        categorias_validas = [choice[0] for choice in Product.CATEGORIAS]
        
        for categoria in categorias_validas:
            with self.subTest(categoria=categoria):
                product_data = {**self.product_data, 'categoria': categoria}
                product = Product.objects.create(**product_data)
                self.assertEqual(product.categoria, categoria)
    
    def test_product_complexidade_choices(self):
        """Testa se todas as complexidades definidas são válidas"""
        complexidades_validas = [choice[0] for choice in Product.COMPLEXIDADE_PRODUCT]
        
        for complexidade in complexidades_validas:
            with self.subTest(complexidade=complexidade):
                product_data = {**self.product_data, 'complexidade_template': complexidade}
                product = Product.objects.create(**product_data)
                self.assertEqual(product.complexidade_template, complexidade)
    
    def test_product_incrementar_uso(self):
        """Testa método incrementar_uso"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.uso_count, 0)
        
        product.incrementar_uso()
        product.refresh_from_db()
        self.assertEqual(product.uso_count, 1)
        
        product.incrementar_uso()
        product.refresh_from_db()
        self.assertEqual(product.uso_count, 2)
    
    def test_product_get_estruturas_incluidas_valid_json(self):
        """Testa método get_estruturas_incluidas com JSON válido"""
        product = Product.objects.create(**self.product_data)
        estruturas = product.get_estruturas_incluidas()
        self.assertEqual(estruturas, [1, 2])
    
    def test_product_get_estruturas_incluidas_invalid_json(self):
        """Testa método get_estruturas_incluidas com JSON inválido"""
        product_data = {
            **self.product_data,
            'configuracao': 'json_invalido'
        }
        product = Product.objects.create(**product_data)
        estruturas = product.get_estruturas_incluidas()
        self.assertEqual(estruturas, [])
    
    def test_product_get_estruturas_incluidas_empty_config(self):
        """Testa método get_estruturas_incluidas com configuração vazia"""
        product_data = {
            **self.product_data,
            'configuracao': {}
        }
        product = Product.objects.create(**product_data)
        estruturas = product.get_estruturas_incluidas()
        self.assertEqual(estruturas, [])
    
    def test_product_campos_opcionais(self):
        """Testa criação de Product apenas com campos obrigatórios"""
        # Remove campos opcionais
        required_data = {k: v for k, v in self.product_data.items() 
                        if k not in ['publico_alvo', 'casos_uso', 'custo_manual']}
        
        product = Product.objects.create(**required_data)
        self.assertEqual(product.publico_alvo, '')
        self.assertEqual(product.casos_uso, '')
        self.assertIsNone(product.custo_manual)
    
    def test_product_campos_opcionais_preenchidos(self):
        """Testa criação de Product com todos os campos preenchidos"""
        dados_completos = {
            **self.product_data,
            'publico_alvo': 'Empresas de tecnologia e startups',
            'casos_uso': 'Estruturação de holdings, proteção patrimonial'
        }
        
        product = Product.objects.create(**dados_completos)
        self.assertEqual(product.publico_alvo, dados_completos['publico_alvo'])
        self.assertEqual(product.casos_uso, dados_completos['casos_uso'])
    
    def test_product_url_validation(self):
        """Testa validação de URL do master_agreement_url"""
        # URL válida
        product = Product(**self.product_data)
        product.full_clean()  # Não deve gerar erro
        
        # URL inválida
        product_data_invalid = {
            **self.product_data,
            'master_agreement_url': 'url_invalida'
        }
        product_invalid = Product(**product_data_invalid)
        with self.assertRaises(ValidationError):
            product_invalid.full_clean()
    
    def test_product_ordering(self):
        """Testa ordenação dos Products por uso_count e commercial_name"""
        product1 = Product.objects.create(
            nome='Produto A',
            commercial_name='A Commercial',
            categoria='TECH',
            descricao='Descrição A',
            master_agreement_url='https://example.com/a.pdf',
            configuracao={},
            tempo_total_implementacao=10,
            uso_count=5
        )
        product2 = Product.objects.create(
            nome='Produto B',
            commercial_name='B Commercial',
            categoria='TRADING',
            descricao='Descrição B',
            master_agreement_url='https://example.com/b.pdf',
            configuracao={},
            tempo_total_implementacao=20,
            uso_count=10
        )
        product3 = Product.objects.create(
            nome='Produto C',
            commercial_name='C Commercial',
            categoria='INVESTMENT',
            descricao='Descrição C',
            master_agreement_url='https://example.com/c.pdf',
            configuracao={},
            tempo_total_implementacao=15,
            uso_count=10
        )
        
        products = list(Product.objects.all())
        # Deve estar ordenado por -uso_count, commercial_name
        # Product2 e Product3 têm uso_count=10, então ordenação por commercial_name
        self.assertEqual(products[0], product2)  # uso_count=10, B Commercial
        self.assertEqual(products[1], product3)  # uso_count=10, C Commercial  
        self.assertEqual(products[2], product1)  # uso_count=5, A Commercial
    
    def test_product_get_categoria_display(self):
        """Testa método get_categoria_display"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.get_categoria_display(), 'Technology')
        
        product.categoria = 'REAL_ESTATE'
        product.save()
        self.assertEqual(product.get_categoria_display(), 'Real Estate')
    
    def test_product_get_complexidade_template_display(self):
        """Testa método get_complexidade_template_display"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.get_complexidade_template_display(), 'Intermediate Configuration')
        
        product.complexidade_template = 'EXPERT'
        product.save()
        self.assertEqual(product.get_complexidade_template_display(), 'Expert Configuration')
    
    def test_product_ativo_default(self):
        """Testa valor padrão do campo ativo"""
        product = Product.objects.create(**self.product_data)
        self.assertTrue(product.ativo)
    
    def test_product_meta_verbose_names(self):
        """Testa nomes verbose do modelo"""
        self.assertEqual(Product._meta.verbose_name, "Product")
        self.assertEqual(Product._meta.verbose_name_plural, "Products")
    
    def test_product_json_field_handling(self):
        """Testa manipulação do campo JSON configuracao"""
        # Teste com dict
        product = Product.objects.create(**self.product_data)
        self.assertIsInstance(product.configuracao, dict)
        
        # Teste com JSON string
        import json
        product_data_json_str = {
            **self.product_data,
            'configuracao': json.dumps({'test': 'value'})
        }
        product2 = Product.objects.create(**product_data_json_str)
        # Django automaticamente converte string JSON para dict
        self.assertIsInstance(product2.configuracao, (dict, str))


class PersonalizedProductModelTest(TestCase):
    """
    Testes para o modelo PersonalizedProduct
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar UBO de teste
        self.ubo = UBO.objects.create(
            nome_completo='João Silva Santos',
            data_nascimento=date(1980, 1, 15),
            nacionalidade='BR',
            tin='CPF12345678901'
        )
        
        # Criar Product de teste
        self.product = Product.objects.create(
            nome='Product Teste',
            categoria='TECH',
            complexidade_template='SIMPLES',
            descricao='Product para testes',
            commercial_name='Commercial Product Test',
            master_agreement_url='https://example.com/agreement',
            configuracao={'test': 'config'},
            tempo_total_implementacao=30,
            custo_automatico=True
        )
        
        # Dados básicos para PersonalizedProduct
        self.pp_data = {
            'nome': 'Produto Personalizado Teste',
            'descricao': 'Descrição do produto personalizado',
            'status': 'DRAFT',
            'base_product': self.product
        }
    
    def test_create_personalized_product_valid(self):
        """Testa criação de PersonalizedProduct com dados válidos"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertEqual(pp.nome, 'Produto Personalizado Teste')
        self.assertEqual(pp.status, 'DRAFT')
        self.assertEqual(pp.version_number, 1)
        self.assertTrue(pp.ativo)
        self.assertEqual(pp.base_product, self.product)
    
    def test_personalized_product_str_representation(self):
        """Testa representação string do PersonalizedProduct"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        expected = f"{pp.nome} (v{pp.version_number}) - {self.product.commercial_name}"
        self.assertEqual(str(pp), expected)
    
    def test_clean_validation_both_bases(self):
        """Testa validação quando ambos base_product e base_structure estão preenchidos"""
        from estruturas_app.models import Estrutura
        
        # Criar uma estrutura de teste
        estrutura = Estrutura.objects.create(
            nome='Estrutura Teste',
            tipo='WYOMING_LLC',
            descricao='Estrutura para testes',
            custo_base=1000.00,
            custo_manutencao=500.00,
            tempo_implementacao=30,
            complexidade=2,
            impacto_tributario_eua='Impacto EUA teste',
            impacto_tributario_brasil='Impacto Brasil teste',
            nivel_confidencialidade=3,
            protecao_patrimonial=3,
            impacto_privacidade='Impacto privacidade teste',
            facilidade_banking=3,
            documentacao_necessaria='Documentação teste'
        )
        
        pp = PersonalizedProduct(
            nome='Teste',
            base_product=self.product,
            base_structure=estrutura
        )
        
        with self.assertRaises(ValidationError):
            pp.clean()
    
    def test_clean_validation_no_base(self):
        """Testa validação quando nenhum base está preenchido"""
        pp = PersonalizedProduct(nome='Teste')
        
        with self.assertRaises(ValidationError):
            pp.clean()
    
    def test_get_base_object_product(self):
        """Testa get_base_object quando base é Product"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertEqual(pp.get_base_object(), self.product)
    
    def test_get_base_type_product(self):
        """Testa get_base_type quando base é Product"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertEqual(pp.get_base_type(), "Product")
    
    def test_get_base_type_structure(self):
        """Testa get_base_type quando base é Structure"""
        from estruturas_app.models import Estrutura
        
        estrutura = Estrutura.objects.create(
            nome='Estrutura Teste',
            tipo='WYOMING_LLC',
            descricao='Estrutura para testes',
            custo_base=1000.00,
            custo_manutencao=500.00,
            tempo_implementacao=30,
            complexidade=2,
            impacto_tributario_eua='Impacto EUA teste',
            impacto_tributario_brasil='Impacto Brasil teste',
            nivel_confidencialidade=3,
            protecao_patrimonial=3,
            impacto_privacidade='Impacto privacidade teste',
            facilidade_banking=3,
            documentacao_necessaria='Documentação teste'
        )
        
        pp_data = self.pp_data.copy()
        pp_data['base_product'] = None
        pp_data['base_structure'] = estrutura
        
        pp = PersonalizedProduct.objects.create(**pp_data)
        self.assertEqual(pp.get_base_type(), "Structure")
    
    def test_get_custo_total_personalizado(self):
        """Testa cálculo de custo com valor personalizado"""
        pp_data = self.pp_data.copy()
        pp_data['custo_personalizado'] = 5000.00
        
        pp = PersonalizedProduct.objects.create(**pp_data)
        self.assertEqual(pp.get_custo_total(), 5000.00)
    
    def test_get_custo_total_automatico(self):
        """Testa cálculo de custo automático"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        # Como o Product não tem método get_custo_total_primeiro_ano implementado,
        # deve retornar 0
        self.assertEqual(pp.get_custo_total(), 0)
    
    def test_create_new_version(self):
        """Testa criação de nova versão"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        
        # Adicionar UBO ao produto original
        PersonalizedProductUBO.objects.create(
            personalized_product=pp,
            ubo=self.ubo,
            ownership_percentage=100.00,
            role='OWNER',
            data_inicio=date.today()
        )
        
        new_version = pp.create_new_version("Teste de nova versão")
        
        self.assertEqual(new_version.version_number, 2)
        self.assertEqual(new_version.parent_version, pp)
        self.assertEqual(new_version.status, 'DRAFT')
        self.assertEqual(new_version.personalizedproductubo_set.count(), 1)
    
    def test_get_ubos_ativos(self):
        """Testa busca de UBOs ativos"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        
        # Adicionar UBO ativo
        PersonalizedProductUBO.objects.create(
            personalized_product=pp,
            ubo=self.ubo,
            ownership_percentage=100.00,
            role='OWNER',
            data_inicio=date.today(),
            ativo=True
        )
        
        ubos_ativos = pp.get_ubos_ativos()
        self.assertEqual(ubos_ativos.count(), 1)
        self.assertIn(self.ubo, ubos_ativos)
    
    def test_get_total_ownership_percentage(self):
        """Testa cálculo de percentual total de propriedade"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        
        # Adicionar UBOs com percentuais
        PersonalizedProductUBO.objects.create(
            personalized_product=pp,
            ubo=self.ubo,
            ownership_percentage=60.00,
            role='OWNER',
            data_inicio=date.today()
        )
        
        # Criar segundo UBO
        ubo2 = UBO.objects.create(
            nome_completo='Maria Santos',
            data_nascimento=date(1985, 5, 20),
            nacionalidade='BR',
            tin='CPF98765432109'
        )
        
        PersonalizedProductUBO.objects.create(
            personalized_product=pp,
            ubo=ubo2,
            ownership_percentage=40.00,
            role='SHAREHOLDER',
            data_inicio=date.today()
        )
        
        total = pp.get_total_ownership_percentage()
        self.assertEqual(total, 100.00)
    
    def test_status_choices(self):
        """Testa choices de status"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        
        # Testar todos os status válidos
        valid_statuses = ['DRAFT', 'ACTIVE', 'INACTIVE', 'ARCHIVED']
        for status in valid_statuses:
            pp.status = status
            pp.save()
            pp.refresh_from_db()
            self.assertEqual(pp.status, status)
    
    def test_configuracao_personalizada_default(self):
        """Testa valor padrão da configuração personalizada"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertEqual(pp.configuracao_personalizada, {})
    
    def test_configuracao_personalizada_custom(self):
        """Testa configuração personalizada customizada"""
        custom_config = {'custom_field': 'custom_value', 'number': 123}
        pp_data = self.pp_data.copy()
        pp_data['configuracao_personalizada'] = custom_config
        
        pp = PersonalizedProduct.objects.create(**pp_data)
        self.assertEqual(pp.configuracao_personalizada, custom_config)
    
    def test_version_number_default(self):
        """Testa valor padrão do número da versão"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertEqual(pp.version_number, 1)
    
    def test_ativo_default(self):
        """Testa valor padrão do campo ativo"""
        pp = PersonalizedProduct.objects.create(**self.pp_data)
        self.assertTrue(pp.ativo)
    
    def test_meta_verbose_names(self):
        """Testa nomes verbose da Meta class"""
        self.assertEqual(PersonalizedProduct._meta.verbose_name, "Personalized Product")
        self.assertEqual(PersonalizedProduct._meta.verbose_name_plural, "Personalized Products")
    
    def test_ordering(self):
        """Testa ordenação padrão"""
        # Criar múltiplos produtos com versões diferentes
        pp1 = PersonalizedProduct.objects.create(
            nome='Produto 1',
            base_product=self.product,
            version_number=1
        )
        
        pp2 = PersonalizedProduct.objects.create(
            nome='Produto 2',
            base_product=self.product,
            version_number=2
        )
        
        products = list(PersonalizedProduct.objects.all())
        # Deve estar ordenado por version_number decrescente
        self.assertEqual(products[0], pp2)
        self.assertEqual(products[1], pp1)


class PersonalizedProductUBOModelTest(TestCase):
    """
    Testes para o modelo PersonalizedProductUBO
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar UBO de teste
        self.ubo = UBO.objects.create(
            nome_completo='João Silva Santos',
            data_nascimento=date(1980, 1, 15),
            nacionalidade='BR',
            tin='CPF12345678901'
        )
        
        # Criar Product de teste
        self.product = Product.objects.create(
            nome='Product Teste',
            categoria='TECH',
            complexidade_template='SIMPLES',
            descricao='Product para testes',
            commercial_name='Commercial Product Test',
            master_agreement_url='https://example.com/agreement',
            configuracao={'test': 'config'},
            tempo_total_implementacao=30,
            custo_automatico=True
        )
        
        # Criar PersonalizedProduct de teste
        self.pp = PersonalizedProduct.objects.create(
            nome='Produto Personalizado Teste',
            base_product=self.product
        )
        
        # Dados básicos para PersonalizedProductUBO
        self.pp_ubo_data = {
            'personalized_product': self.pp,
            'ubo': self.ubo,
            'ownership_percentage': 100.00,
            'role': 'OWNER',
            'data_inicio': date.today()
        }
    
    def test_create_personalized_product_ubo_valid(self):
        """Testa criação de PersonalizedProductUBO com dados válidos"""
        pp_ubo = PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
        self.assertEqual(pp_ubo.personalized_product, self.pp)
        self.assertEqual(pp_ubo.ubo, self.ubo)
        self.assertEqual(pp_ubo.ownership_percentage, 100.00)
        self.assertEqual(pp_ubo.role, 'OWNER')
        self.assertTrue(pp_ubo.ativo)
    
    def test_personalized_product_ubo_str_representation(self):
        """Testa representação string do PersonalizedProductUBO"""
        pp_ubo = PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
        expected = f"{self.ubo.nome_completo} - Owner (100.0%)"
        self.assertEqual(str(pp_ubo), expected)
    
    def test_str_representation_without_percentage(self):
        """Testa representação string sem percentual"""
        pp_ubo_data = self.pp_ubo_data.copy()
        pp_ubo_data['ownership_percentage'] = None
        
        pp_ubo = PersonalizedProductUBO.objects.create(**pp_ubo_data)
        expected = f"{self.ubo.nome_completo} - Owner"
        self.assertEqual(str(pp_ubo), expected)
    
    def test_role_choices(self):
        """Testa choices de role"""
        pp_ubo = PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
        
        # Testar todos os roles válidos
        valid_roles = ['OWNER', 'BENEFICIARY', 'DIRECTOR', 'SHAREHOLDER', 'TRUSTEE', 'OTHER']
        for role in valid_roles:
            pp_ubo.role = role
            pp_ubo.save()
            pp_ubo.refresh_from_db()
            self.assertEqual(pp_ubo.role, role)
    
    def test_ownership_percentage_validation_min(self):
        """Testa validação de percentual mínimo"""
        pp_ubo_data = self.pp_ubo_data.copy()
        pp_ubo_data['ownership_percentage'] = 0.005  # Menor que 0.01
        
        pp_ubo = PersonalizedProductUBO(**pp_ubo_data)
        with self.assertRaises(ValidationError):
            pp_ubo.full_clean()
    
    def test_ownership_percentage_validation_max(self):
        """Testa validação de percentual máximo"""
        pp_ubo_data = self.pp_ubo_data.copy()
        pp_ubo_data['ownership_percentage'] = 100.01  # Maior que 100
        
        pp_ubo = PersonalizedProductUBO(**pp_ubo_data)
        with self.assertRaises(ValidationError):
            pp_ubo.full_clean()
    
    def test_clean_validation_data_fim_anterior(self):
        """Testa validação quando data_fim é anterior a data_inicio"""
        pp_ubo_data = self.pp_ubo_data.copy()
        pp_ubo_data['data_fim'] = date(2020, 1, 1)  # Anterior a data_inicio
        
        pp_ubo = PersonalizedProductUBO(**pp_ubo_data)
        with self.assertRaises(ValidationError):
            pp_ubo.clean()
    
    def test_clean_validation_data_fim_valida(self):
        """Testa validação quando data_fim é posterior a data_inicio"""
        pp_ubo_data = self.pp_ubo_data.copy()
        pp_ubo_data['data_fim'] = date(2025, 12, 31)  # Posterior a data_inicio
        
        pp_ubo = PersonalizedProductUBO(**pp_ubo_data)
        # Não deve levantar exceção
        pp_ubo.clean()
    
    def test_unique_together_constraint(self):
        """Testa constraint unique_together"""
        # Criar primeiro registro
        PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
        
        # Tentar criar segundo registro com mesma combinação
        with self.assertRaises(Exception):  # IntegrityError
            PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
    
    def test_ativo_default(self):
        """Testa valor padrão do campo ativo"""
        pp_ubo = PersonalizedProductUBO.objects.create(**self.pp_ubo_data)
        self.assertTrue(pp_ubo.ativo)
    
    def test_role_default(self):
        """Testa valor padrão do role"""
        pp_ubo_data = self.pp_ubo_data.copy()
        del pp_ubo_data['role']  # Remover role para testar padrão
        
        pp_ubo = PersonalizedProductUBO.objects.create(**pp_ubo_data)
        self.assertEqual(pp_ubo.role, 'OWNER')
    
    def test_meta_verbose_names(self):
        """Testa nomes verbose da Meta class"""
        self.assertEqual(PersonalizedProductUBO._meta.verbose_name, "Personalized Product UBO")
        self.assertEqual(PersonalizedProductUBO._meta.verbose_name_plural, "Personalized Product UBOs")


class ServiceModelTest(TestCase):
    """Test cases for Service model"""
    
    def setUp(self):
        """Set up test data"""
        # Criar uma estrutura de teste
        from .models import Estrutura
        self.estrutura = Estrutura.objects.create(
            nome='Test Structure',
            tipo='WYOMING_DAO_LLC',
            descricao='Test structure for service testing',
            custo_base=5000.00,
            custo_manutencao=1000.00,
            tempo_implementacao=30,
            complexidade=3,
            impacto_tributario_eua='Test tax impact USA',
            impacto_tributario_brasil='Test tax impact Brazil',
            nivel_confidencialidade=3,
            protecao_patrimonial=3,
            impacto_privacidade='Test privacy impact',
            facilidade_banking=3,
            documentacao_necessaria='Test documentation required',
            ativo=True
        )
        
        # Criar Product de teste
        self.product = Product.objects.create(
            nome='Test Product',
            categoria='TECH',
            complexidade_template='BASIC',
            descricao='Test product for service testing',
            commercial_name='Test Commercial Product',
            master_agreement_url='https://example.com/agreement',
            configuracao={'test': 'config'},
            custo_automatico=False,
            custo_manual=5000.00,
            tempo_total_implementacao=30,
            ativo=True
        )
        
        # Criar Service de teste
        self.service = Service.objects.create(
            service_name='Legal Formation Service',
            description='Complete legal formation service for offshore structures',
            service_type='LEGAL',
            cost=2500.00,
            estimated_duration=15,
            requirements={'documents': ['passport', 'proof_of_address']},
            deliverables={'certificates': ['incorporation', 'good_standing']},
            status='ACTIVE',
            associated_product=self.product,
            ativo=True
        )
    
    def test_service_creation(self):
        """Test service creation with valid data"""
        service = Service.objects.create(
            service_name='Tax Compliance Service',
            description='Annual tax compliance and filing service',
            service_type='TAX',
            cost=1500.00,
            estimated_duration=10,
            status='ACTIVE'
        )
        
        self.assertEqual(service.service_name, 'Tax Compliance Service')
        self.assertEqual(service.service_type, 'TAX')
        self.assertEqual(service.cost, 1500.00)
        self.assertEqual(service.status, 'ACTIVE')
        self.assertTrue(service.ativo)
    
    def test_service_string_representation(self):
        """Test service string representation"""
        expected = f"{self.service.service_name} ({self.service.get_service_type_display()})"
        self.assertEqual(str(self.service), expected)
    
    def test_service_association_type_product(self):
        """Test get_association_type method with product"""
        self.assertEqual(self.service.get_association_type(), "Product")
    
    def test_service_association_type_structure(self):
        """Test get_association_type method with structure"""
        service = Service.objects.create(
            service_name='Structure Maintenance',
            description='Annual structure maintenance service',
            service_type='MAINTENANCE',
            associated_structure=self.estrutura
        )
        self.assertEqual(service.get_association_type(), "Structure")
    
    def test_service_association_type_standalone(self):
        """Test get_association_type method with no association"""
        service = Service.objects.create(
            service_name='Consulting Service',
            description='General consulting service',
            service_type='CONSULTING'
        )
        self.assertEqual(service.get_association_type(), "Standalone")
    
    def test_service_is_available_for_association(self):
        """Test is_available_for_association method"""
        # Active service should be available
        self.assertTrue(self.service.is_available_for_association())
        
        # Inactive service should not be available
        self.service.status = 'INACTIVE'
        self.service.save()
        self.assertFalse(self.service.is_available_for_association())
        
        # Draft service should not be available
        self.service.status = 'DRAFT'
        self.service.save()
        self.assertFalse(self.service.is_available_for_association())
    
    def test_service_get_associated_entity(self):
        """Test get_associated_entity method"""
        # Service associated with product
        self.assertEqual(self.service.associated_product, self.product)
        
        # Service associated with structure
        service = Service.objects.create(
            service_name='Structure Service',
            description='Structure-specific service',
            service_type='ADMINISTRATIVE',
            associated_structure=self.estrutura
        )
        self.assertEqual(service.associated_structure, self.estrutura)
        
        # Standalone service
        standalone_service = Service.objects.create(
            service_name='Standalone Service',
            description='Standalone service',
            service_type='CONSULTING'
        )
        self.assertIsNone(standalone_service.associated_product)
        self.assertIsNone(standalone_service.associated_structure)
    
    def test_service_create_personalized_service(self):
        """Test create_personalized_service method"""
        personalized = self.service.create_personalized_service()
        
        self.assertIsNotNone(personalized)
        self.assertEqual(personalized.base_product, self.product)
        self.assertEqual(personalized.status, 'DRAFT')
        self.assertIn('service_id', personalized.configuracao_personalizada)
        self.assertEqual(personalized.configuracao_personalizada['service_id'], self.service.id)
    
    def test_service_clean_validation(self):
        """Test service clean method validation"""
        # Test that service can be created without validation errors
        service = Service(
            service_name='Valid Service',
            description='Service with valid data',
            service_type='LEGAL',
            associated_product=self.product
        )
        
        # Should not raise ValidationError
        try:
            service.clean()
        except ValidationError:
            self.fail("Service.clean() raised ValidationError unexpectedly!")
    
    def test_service_cost_validation(self):
        """Test service cost validation"""
        # Test that service with valid cost can be created
        service = Service(
            service_name='Valid Cost Service',
            description='Service with valid cost',
            service_type='LEGAL',
            cost=100.00
        )
        
        # Should not raise ValidationError
        try:
            service.clean()
        except ValidationError:
            self.fail("Service.clean() raised ValidationError unexpectedly!")
    
    def test_service_duration_validation(self):
        """Test service duration validation"""
        # Test that service with valid duration can be created
        service = Service(
            service_name='Valid Duration Service',
            description='Service with valid duration',
            service_type='LEGAL',
            estimated_duration=10
        )
        
        # Should not raise ValidationError
        try:
            service.clean()
        except ValidationError:
            self.fail("Service.clean() raised ValidationError unexpectedly!")


class ServiceActivityModelTest(TestCase):
    """Test cases for ServiceActivity model"""
    
    def setUp(self):
        """Set up test data"""
        # Criar Service de teste
        self.service = Service.objects.create(
            service_name='Test Service',
            description='Test service for activity testing',
            service_type='LEGAL',
            status='ACTIVE'
        )
        
        # Criar ServiceActivity de teste
        self.activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='Document Review',
            activity_description='Review and validate client documents',
            start_date=date(2024, 1, 15),
            due_date=date(2024, 1, 30),
            status='PLANNED',
            priority='HIGH',
            responsible_person='John Doe',
            estimated_hours=8.0
        )
    
    def test_activity_creation(self):
        """Test activity creation with valid data"""
        activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='Client Meeting',
            activity_description='Initial consultation with client',
            start_date=date(2024, 2, 1),
            status='PLANNED',
            priority='MEDIUM',
            responsible_person='Jane Smith'
        )
        
        self.assertEqual(activity.activity_title, 'Client Meeting')
        self.assertEqual(activity.status, 'PLANNED')
        self.assertEqual(activity.priority, 'MEDIUM')
        self.assertTrue(activity.ativo)
    
    def test_activity_string_representation(self):
        """Test activity string representation"""
        expected = f"{self.activity.activity_title} - {self.service.service_name}"
        self.assertEqual(str(self.activity), expected)
    
    def test_activity_is_overdue(self):
        """Test is_overdue method"""
        # Activity with past due date should be overdue
        past_activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='Past Activity',
            activity_description='Activity with past due date',
            start_date=date(2023, 12, 1),
            due_date=date(2023, 12, 15),
            status='IN_PROGRESS',
            priority='HIGH',
            responsible_person='Test Person'
        )
        self.assertTrue(past_activity.is_overdue())
        
        # Activity with future due date should not be overdue
        future_date = timezone.now().date() + timezone.timedelta(days=30)
        future_activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='Future Activity',
            activity_description='Activity with future due date',
            start_date=timezone.now().date(),
            due_date=future_date,
            status='PLANNED',
            priority='MEDIUM',
            responsible_person='Test Person'
        )
        self.assertFalse(future_activity.is_overdue())
        
        # Activity without due date should not be overdue
        no_due_activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='No Due Date Activity',
            activity_description='Activity without due date',
            start_date=timezone.now().date(),
            status='PLANNED',
            priority='LOW',
            responsible_person='Test Person'
        )
        self.assertFalse(no_due_activity.is_overdue())
    
    def test_activity_get_progress_percentage(self):
        """Test get_progress_percentage method"""
        # Planned activity should be 0%
        self.assertEqual(self.activity.get_progress_percentage(), 0)
        
        # In progress activity should be 50%
        self.activity.status = 'IN_PROGRESS'
        self.activity.save()
        self.assertEqual(self.activity.get_progress_percentage(), 50)
        
        # Completed activity should be 100%
        self.activity.status = 'COMPLETED'
        self.activity.save()
        self.assertEqual(self.activity.get_progress_percentage(), 100)
        
        # On hold activity should be 25%
        self.activity.status = 'ON_HOLD'
        self.activity.save()
        self.assertEqual(self.activity.get_progress_percentage(), 25)
        
        # Cancelled activity should be 0%
        self.activity.status = 'CANCELLED'
        self.activity.save()
        self.assertEqual(self.activity.get_progress_percentage(), 0)
    
    def test_activity_get_status_color(self):
        """Test get_status_color method"""
        # Test different status colors
        status_colors = {
            'PLANNED': '#6c757d',
            'IN_PROGRESS': '#007bff',
            'COMPLETED': '#28a745',
            'ON_HOLD': '#ffc107',
            'CANCELLED': '#dc3545'
        }
        
        for status, expected_color in status_colors.items():
            self.activity.status = status
            self.activity.save()
            self.assertEqual(self.activity.get_status_color(), expected_color)
    
    def test_activity_get_priority_color(self):
        """Test get_priority_color method"""
        # Test different priority colors
        priority_colors = {
            'LOW': '#28a745',
            'MEDIUM': '#ffc107',
            'HIGH': '#fd7e14',
            'URGENT': '#dc3545'
        }
        
        for priority, expected_color in priority_colors.items():
            self.activity.priority = priority
            self.activity.save()
            self.assertEqual(self.activity.get_priority_color(), expected_color)
    
    def test_activity_mark_completed(self):
        """Test mark_completed method"""
        # Mark activity as completed
        completion_date = date(2024, 1, 25)
        self.activity.mark_completed(completion_date)
        
        self.assertEqual(self.activity.status, 'COMPLETED')
        self.assertEqual(self.activity.completion_date, completion_date)
        
        # Mark completed without specific date (should use today)
        new_activity = ServiceActivity.objects.create(
            service=self.service,
            activity_title='New Activity',
            activity_description='Activity to be completed',
            start_date=date(2024, 2, 1),
            status='IN_PROGRESS',
            priority='MEDIUM',
            responsible_person='Test Person'
        )
        new_activity.mark_completed()
        
        self.assertEqual(new_activity.status, 'COMPLETED')
        self.assertEqual(new_activity.completion_date, timezone.now().date())
    
    def test_activity_clean_validation(self):
        """Test activity clean method validation"""
        # Test that activity can be created without validation errors
        activity = ServiceActivity(
            service=self.service,
            activity_title='Valid Activity',
            activity_description='Activity with valid data',
            start_date=date(2024, 1, 1),
            completion_date=date(2024, 1, 15),
            status='COMPLETED',
            priority='MEDIUM',
            responsible_person='Test Person'
        )
        
        # Should not raise ValidationError
        try:
            activity.clean()
        except ValidationError:
            self.fail("ServiceActivity.clean() raised ValidationError unexpectedly!")
        
        # Test another valid activity
        activity2 = ServiceActivity(
            service=self.service,
            activity_title='Valid Dates Activity',
            activity_description='Activity with valid date range',
            start_date=date(2024, 1, 1),
            due_date=date(2024, 1, 15),
            status='PLANNED',
            priority='MEDIUM',
            responsible_person='Test Person'
        )
        
        # Should not raise ValidationError
        try:
            activity2.clean()
        except ValidationError:
            self.fail("ServiceActivity.clean() raised ValidationError unexpectedly!")


class AlertaJurisdicaoModelTest(TestCase):
    """Test cases for enhanced AlertaJurisdicao model"""
    
    def setUp(self):
        """Set up test data"""
        from .models import Estrutura
        
        # Criar estrutura de teste
        self.estrutura = Estrutura.objects.create(
            nome='Test Structure',
            tipo='WYOMING_DAO_LLC',
            descricao='Test structure for alert testing',
            custo_base=5000.00,
            custo_manutencao=1000.00,
            tempo_implementacao=30,
            complexidade=3,
            impacto_tributario_eua='Test tax impact USA',
            impacto_tributario_brasil='Test tax impact Brazil',
            nivel_confidencialidade=3,
            protecao_patrimonial=3,
            impacto_privacidade='Test privacy impact',
            facilidade_banking=3,
            documentacao_necessaria='Test documentation required',
            ativo=True
        )
        
        # Criar UBO de teste
        self.ubo = UBO.objects.create(
            nome_completo='John Doe',
            data_nascimento=date(1980, 5, 15),
            nacionalidade='US',
            tin='123456789',
            email='john.doe@example.com',
            ativo=True
        )
        
        # Criar Service de teste
        self.service = Service.objects.create(
            service_name='Compliance Service',
            description='Annual compliance service',
            service_type='COMPLIANCE',
            status='ACTIVE'
        )
        
        # Criar AlertaJurisdicao de teste
        self.alert = AlertaJurisdicao.objects.create(
            titulo='Annual Tax Filing',
            descricao='Annual corporate tax filing requirement',
            jurisdicao='US',
            tipo_alerta='TAX',
            deadline_type='RECURRING',
            recurrence_pattern='ANNUAL',
            next_deadline=date(2024, 4, 15),
            prioridade=4,
            service_connection=self.service,
            ativo=True
        )
        self.alert.estruturas_aplicaveis.add(self.estrutura)
        self.alert.ubos_aplicaveis.add(self.ubo)
    
    def test_alert_creation(self):
        """Test alert creation with enhanced fields"""
        alert = AlertaJurisdicao.objects.create(
            titulo='License Renewal',
            descricao='Business license renewal requirement',
            jurisdicao='BR',
            tipo_alerta='RENEWAL',
            deadline_type='SINGLE',
            single_deadline=date(2024, 12, 31),
            prioridade=3,
            advance_notice_days=60,
            template_url='https://example.com/template',
            compliance_url='https://example.com/compliance'
        )
        
        self.assertEqual(alert.titulo, 'License Renewal')
        self.assertEqual(alert.deadline_type, 'SINGLE')
        self.assertEqual(alert.single_deadline, date(2024, 12, 31))
        self.assertEqual(alert.advance_notice_days, 60)
        self.assertTrue(alert.ativo)
    
    def test_alert_string_representation(self):
        """Test alert string representation"""
        expected = f"{self.alert.get_jurisdicao_display()}: {self.alert.titulo}"
        self.assertEqual(str(self.alert), expected)
    
    def test_alert_clean_validation_single_deadline(self):
        """Test clean validation for single deadline type"""
        # Single deadline without date should raise ValidationError
        alert = AlertaJurisdicao(
            titulo='Invalid Single Alert',
            descricao='Alert without single deadline date',
            jurisdicao='US',
            tipo_alerta='DEADLINE',
            deadline_type='SINGLE'
        )
        
        with self.assertRaises(ValidationError):
            alert.clean()
        
        # Single deadline with recurrence pattern should raise ValidationError
        alert = AlertaJurisdicao(
            titulo='Invalid Single Alert',
            descricao='Alert with recurrence pattern',
            jurisdicao='US',
            tipo_alerta='DEADLINE',
            deadline_type='SINGLE',
            single_deadline=date(2024, 6, 1),
            recurrence_pattern='MONTHLY'
        )
        
        with self.assertRaises(ValidationError):
            alert.clean()
    
    def test_alert_clean_validation_recurring_deadline(self):
        """Test clean validation for recurring deadline type"""
        # Recurring deadline without pattern should raise ValidationError
        alert = AlertaJurisdicao(
            titulo='Invalid Recurring Alert',
            descricao='Alert without recurrence pattern',
            jurisdicao='US',
            tipo_alerta='DEADLINE',
            deadline_type='RECURRING'
        )
        
        with self.assertRaises(ValidationError):
            alert.clean()
        
        # Recurring deadline with single deadline should raise ValidationError
        alert = AlertaJurisdicao(
            titulo='Invalid Recurring Alert',
            descricao='Alert with single deadline',
            jurisdicao='US',
            tipo_alerta='DEADLINE',
            deadline_type='RECURRING',
            recurrence_pattern='MONTHLY',
            single_deadline=date(2024, 6, 1)
        )
        
        with self.assertRaises(ValidationError):
            alert.clean()
    
    def test_alert_calculate_next_deadline(self):
        """Test calculate_next_deadline method"""
        # Test monthly recurrence
        self.alert.recurrence_pattern = 'MONTHLY'
        self.alert.last_completed = date(2024, 1, 15)
        next_deadline = self.alert.calculate_next_deadline()
        self.assertEqual(next_deadline, date(2024, 2, 15))
        
        # Test quarterly recurrence
        self.alert.recurrence_pattern = 'QUARTERLY'
        next_deadline = self.alert.calculate_next_deadline()
        self.assertEqual(next_deadline, date(2024, 4, 15))
        
        # Test annual recurrence
        self.alert.recurrence_pattern = 'ANNUAL'
        next_deadline = self.alert.calculate_next_deadline()
        self.assertEqual(next_deadline, date(2025, 1, 15))
    
    def test_alert_is_overdue(self):
        """Test is_overdue method"""
        # Alert with past deadline should be overdue
        self.alert.next_deadline = date(2023, 12, 1)
        self.alert.save()
        self.assertTrue(self.alert.is_overdue())
        
        # Alert with future deadline should not be overdue
        future_date = timezone.now().date() + timezone.timedelta(days=30)
        self.alert.next_deadline = future_date
        self.alert.save()
        self.assertFalse(self.alert.is_overdue())
        
        # Alert without deadline should not be overdue
        self.alert.next_deadline = None
        self.alert.save()
        self.assertFalse(self.alert.is_overdue())
    
    def test_alert_days_until_deadline(self):
        """Test days_until_deadline method"""
        # Set a future deadline
        future_date = timezone.now().date() + timezone.timedelta(days=30)
        self.alert.next_deadline = future_date
        self.alert.save()
        
        self.assertEqual(self.alert.days_until_deadline(), 30)
        
        # Alert without deadline should return None
        self.alert.next_deadline = None
        self.alert.save()
        self.assertIsNone(self.alert.days_until_deadline())
    
    def test_alert_needs_advance_notice(self):
        """Test needs_advance_notice method"""
        # Alert within advance notice period should need notice
        notice_date = timezone.now().date() + timezone.timedelta(days=15)
        self.alert.next_deadline = notice_date
        self.alert.advance_notice_days = 30
        self.alert.save()
        
        self.assertTrue(self.alert.needs_advance_notice())
        
        # Alert outside advance notice period should not need notice
        far_date = timezone.now().date() + timezone.timedelta(days=60)
        self.alert.next_deadline = far_date
        self.alert.save()
        
        self.assertFalse(self.alert.needs_advance_notice())
    
    def test_alert_get_status_display(self):
        """Test get_status_display method"""
        # Test overdue status
        self.alert.next_deadline = date(2023, 12, 1)
        self.alert.save()
        self.assertEqual(self.alert.get_status_display(), "Overdue")
        
        # Test due soon status
        soon_date = timezone.now().date() + timezone.timedelta(days=15)
        self.alert.next_deadline = soon_date
        self.alert.advance_notice_days = 30
        self.alert.save()
        self.assertEqual(self.alert.get_status_display(), "Due Soon")
        
        # Test scheduled status
        future_date = timezone.now().date() + timezone.timedelta(days=60)
        self.alert.next_deadline = future_date
        self.alert.save()
        self.assertEqual(self.alert.get_status_display(), "Scheduled")
        
        # Test no deadline status
        self.alert.next_deadline = None
        self.alert.save()
        self.assertEqual(self.alert.get_status_display(), "No Deadline")
    
    def test_alert_mark_completed(self):
        """Test mark_completed method"""
        # Mark alert as completed
        completion_date = date(2024, 4, 15)
        self.alert.mark_completed(completion_date)
        
        self.assertEqual(self.alert.last_completed, completion_date)
        # Next deadline should be calculated for recurring alerts
        self.assertIsNotNone(self.alert.next_deadline)
        
        # Mark completed without specific date (should use today)
        self.alert.mark_completed()
        self.assertEqual(self.alert.last_completed, timezone.now().date())
    
    def test_alert_get_applicable_entities(self):
        """Test get_applicable_entities method"""
        entities = self.alert.get_applicable_entities()
        
        self.assertIn(self.estrutura, entities)
        self.assertIn(self.ubo, entities)
        self.assertEqual(len(entities), 2)
    
    def test_alert_create_service_activity(self):
        """Test create_service_activity method"""
        activity = self.alert.create_service_activity(
            activity_title="Custom Alert Activity",
            responsible_person="Compliance Officer"
        )
        
        self.assertIsNotNone(activity)
        self.assertEqual(activity.service, self.service)
        self.assertEqual(activity.activity_title, "Custom Alert Activity")
        self.assertEqual(activity.responsible_person, "Compliance Officer")
        self.assertEqual(activity.due_date, self.alert.next_deadline)
        self.assertEqual(activity.priority, 'HIGH')  # Priority 4 maps to HIGH
        
        # Alert without service connection should return None
        alert_no_service = AlertaJurisdicao.objects.create(
            titulo='No Service Alert',
            descricao='Alert without service connection',
            jurisdicao='US',
            tipo_alerta='COMPLIANCE'
        )
        
        activity = alert_no_service.create_service_activity()
        self.assertIsNone(activity)

