from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField


class Client(models.Model):
    """
    Cliente no sistema de relacionamento corporativo.
    Representa empresas/entidades que contratam serviços.
    """

    company_name = models.CharField(
        max_length=120, help_text="Nome da empresa cliente"
    )
    address = models.TextField(help_text="Endereço completo do cliente")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data de criação do registro"
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    """
    Contato dentro de um cliente.
    Representa pessoas de contato para comunicação.
    """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="contacts",
        help_text="Cliente ao qual este contato pertence",
    )
    name = models.CharField(
        max_length=120, help_text="Nome completo do contato"
    )
    role = models.CharField(
        max_length=80, help_text="Função/cargo (ex.: Diretor Financeiro)"
    )
    phone = models.CharField(
        max_length=40, blank=True, help_text="Número de telefone"
    )
    email = models.EmailField(help_text="Email para contato")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.client.company_name}"


class RelationshipStructure(models.Model):
    """
    Relacionamento entre uma Structure e um Client.
    Criado automaticamente quando um PersonalizedProduct é aprovado.
    """

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("ARCHIVED", "Archived"),
    ]

    structure = models.ForeignKey(
        "corporate.Structure",
        on_delete=models.CASCADE,
        help_text="Estrutura legal relacionada",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        help_text="Cliente proprietário da estrutura",
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="ACTIVE",
        help_text="Status do relacionamento",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data de criação do relacionamento"
    )

    class Meta:
        verbose_name = "Relationship Structure"
        verbose_name_plural = "Relationship Structures"
        unique_together = ["structure", "client"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.structure.nome} - {self.client.company_name}"


class Service(models.Model):
    """
    Serviço que pode ser executado para um cliente.
    Migrado de corporate.Service com suporte multi-moeda.
    """

    name = models.CharField(max_length=120, help_text="Nome do serviço")
    description = models.TextField(
        blank=True, help_text="Descrição detalhada do serviço"
    )

    # Preços multi-moeda (USD, BRL, EUR)
    service_price = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        help_text="Preço do serviço",
    )
    regulator_fee = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        help_text="Taxa regulatória/governamental",
    )

    # Cargos e responsabilidades
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="Usuário responsável pela execução",
    )
    counterparty_name = models.CharField(
        max_length=120, help_text="Nome do órgão/entidade receptora"
    )
    informed = models.ManyToManyField(
        Contact,
        blank=True,
        help_text="Contatos do cliente a serem notificados",
    )

    # Relacionamentos
    relationship_structure = models.ForeignKey(
        RelationshipStructure,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Estrutura relacionada (opcional)",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.counterparty_name}"

    def get_total_cost(self):
        """Calcula custo total (serviço + taxa regulatória)"""
        return self.service_price + self.regulator_fee


class ServiceActivity(models.Model):
    """
    Atividade específica dentro de um serviço.
    Permite rastreamento detalhado da execução.
    """

    STATUS_CHOICES = [
        ("TODO", "To do"),
        ("DONE", "Done"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="activities",
        help_text="Serviço ao qual esta atividade pertence",
    )
    order = models.PositiveSmallIntegerField(
        help_text="Ordem de execução da atividade"
    )
    name = models.CharField(max_length=120, help_text="Nome da atividade")
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default="TODO",
        help_text="Status da atividade",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Activity"
        verbose_name_plural = "Service Activities"
        ordering = ["order"]
        unique_together = ["service", "order"]

    def __str__(self):
        return f"{self.service.name} - {self.order}. {self.name}"


class WebhookLog(models.Model):
    """
    Log de tentativas de webhook para auditoria e retentativas.
    """

    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("PENDING", "Pending"),
    ]

    event_type = models.CharField(
        max_length=50,
        help_text="Tipo do evento (ex: personalized_product_approved)",
    )
    payload = models.JSONField(help_text="Payload enviado no webhook")
    url = models.URLField(help_text="URL de destino do webhook")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
        help_text="Status da tentativa",
    )
    response_status_code = models.PositiveIntegerField(
        null=True, blank=True, help_text="Código de status HTTP da resposta"
    )
    response_body = models.TextField(
        blank=True, help_text="Corpo da resposta HTTP"
    )
    error_message = models.TextField(
        blank=True, help_text="Mensagem de erro se houver falha"
    )
    attempt_count = models.PositiveIntegerField(
        default=1, help_text="Número de tentativas realizadas"
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data da primeira tentativa"
    )
    last_attempt_at = models.DateTimeField(
        auto_now=True, help_text="Data da última tentativa"
    )

    class Meta:
        verbose_name = "Webhook Log"
        verbose_name_plural = "Webhook Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.status} ({self.attempt_count} attempts)"
