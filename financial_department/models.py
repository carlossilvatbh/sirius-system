from django.core.validators import MinValueValidator
from django.db import models


class EntityPrice(models.Model):
    """
    Manages pricing for legal entities
    Centralizes cost management from Entity model
    """

    BASE_CURRENCIES = [
        ('USD', 'US Dollar'),
        ('BRL', 'Brazilian Real'),
        ('EUR', 'Euro'),
    ]

    entity = models.OneToOneField('corporate.Entity', on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=3, choices=BASE_CURRENCIES)

    # Price markup (either percentage or fixed amount)
    MARKUP_TYPES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed Amount')
    ]
    markup_type = models.CharField(max_length=10, choices=MARKUP_TYPES)
    markup_value = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entity Price"
        verbose_name_plural = "Entity Prices"
        indexes = [
            models.Index(fields=["entity"]),
            models.Index(fields=["base_currency"]),
        ]

    def __str__(self):
        return f"{self.entity.name} - {self.get_base_currency_display()}"

    def get_total_cost(self):
        """Calculate total cost including markup"""
        base_cost = sum(cost.value for cost in self.costs.all())
        
        if self.markup_type == 'PERCENTAGE':
            return base_cost * (1 + self.markup_value / 100)
        else:  # FIXED
            return base_cost + self.markup_value


class IncorporationCost(models.Model):
    """
    Individual cost components for entity incorporation
    One-to-many relationship with EntityPrice
    """

    COST_TYPES = [
        ('LEGAL_FEE', 'Legal Fee'),
        ('SERVICE_PROVIDER', 'Service Provider'),
    ]

    entity_price = models.ForeignKey(
        EntityPrice, 
        on_delete=models.CASCADE, 
        related_name='costs'
    )
    name = models.CharField(max_length=200, help_text="Cost component name")
    cost_type = models.CharField(max_length=20, choices=COST_TYPES)
    value = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Incorporation Cost"
        verbose_name_plural = "Incorporation Costs"
        ordering = ["entity_price", "name"]
        indexes = [
            models.Index(fields=["entity_price"]),
            models.Index(fields=["cost_type"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_cost_type_display()}: {self.value}"


class ServicePrice(models.Model):
    """
    Manages pricing for services
    Same structure as EntityPrice but for services
    """

    BASE_CURRENCIES = [
        ('USD', 'US Dollar'),
        ('BRL', 'Brazilian Real'),
        ('EUR', 'Euro'),
    ]

    MARKUP_TYPES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed Amount')
    ]

    service = models.OneToOneField(
        'corporate_relationship.Service', 
        on_delete=models.CASCADE
    )
    base_currency = models.CharField(max_length=3, choices=BASE_CURRENCIES)
    markup_type = models.CharField(max_length=10, choices=MARKUP_TYPES)
    markup_value = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Price"
        verbose_name_plural = "Service Prices"
        indexes = [
            models.Index(fields=["service"]),
            models.Index(fields=["base_currency"]),
        ]

    def __str__(self):
        return f"{self.service.name} - {self.get_base_currency_display()}"

    def get_total_cost(self):
        """Calculate total cost including markup"""
        base_cost = sum(cost.value for cost in self.costs.all())
        
        if self.markup_type == 'PERCENTAGE':
            return base_cost * (1 + self.markup_value / 100)
        else:  # FIXED
            return base_cost + self.markup_value


class ServiceCost(models.Model):
    """
    Individual cost components for services
    """

    COST_TYPES = [
        ('LEGAL_FEE', 'Legal Fee'),
        ('SERVICE_PROVIDER', 'Service Provider'),
    ]

    service_price = models.ForeignKey(
        ServicePrice, 
        on_delete=models.CASCADE, 
        related_name='costs'
    )
    name = models.CharField(max_length=200)
    cost_type = models.CharField(max_length=20, choices=COST_TYPES)
    value = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Cost"
        verbose_name_plural = "Service Costs"
        ordering = ["service_price", "name"]
        indexes = [
            models.Index(fields=["service_price"]),
            models.Index(fields=["cost_type"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_cost_type_display()}: {self.value}"

