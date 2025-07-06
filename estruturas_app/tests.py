from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from .models import UBO, Successor, Product


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

