class EntityOwnership(models.Model):
    """
    Manages ownership relationships within a Structure
    Handles both UBO → Entity and Entity → Entity ownership
    Enhanced with Corporate Name, Hash Number, and Share Values
    """

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, related_name='entity_ownerships')

    # Owner can be either UBO or Entity
    owner_ubo = models.ForeignKey(
        'parties.Party', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        help_text="UBO owner"
    )
    owner_entity = models.ForeignKey(
        Entity, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='ownerships_as_owner',
        help_text="Entity owner"
    )

    # Owned entity
    owned_entity = models.ForeignKey(
        Entity, 
        on_delete=models.CASCADE, 
        related_name='ownerships_as_owned'
    )

    # Corporate identification (FASE 2)
    corporate_name = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Corporate name when entity is used in structure"
    )
    hash_number = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Hash number when entity is used in structure"
    )

    # Share management
    owned_shares = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of shares owned by this owner"
    )
    ownership_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ownership percentage"
    )

    # Share valuation (FASE 3)
    share_value_usd = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.01)],
        help_text="Value per share in USD"
    )
    share_value_eur = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.01)],
        help_text="Value per share in EUR"
    )

    # Total values (calculated fields)
    total_value_usd = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Total value of owned shares in USD"
    )
    total_value_eur = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Total value of owned shares in EUR"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entity Ownership"
        verbose_name_plural = "Entity Ownerships"
        unique_together = ['structure', 'owner_ubo', 'owner_entity', 'owned_entity']
        indexes = [
            models.Index(fields=["structure"]),
            models.Index(fields=["owned_entity"]),
            models.Index(fields=["owner_ubo"]),
            models.Index(fields=["owner_entity"]),
        ]

    def __str__(self):
        owner_name = ""
        if self.owner_ubo:
            owner_name = str(self.owner_ubo)
        elif self.owner_entity:
            owner_name = str(self.owner_entity)
        
        percentage = self.ownership_percentage or 0
        return f"{owner_name} owns {percentage}% of {self.owned_entity.name}"

    def clean(self):
        super().clean()
        # Validate that exactly one owner type is specified
        owner_count = sum([bool(self.owner_ubo), bool(self.owner_entity)])
        if owner_count != 1:
            raise ValidationError("Must specify exactly one owner (UBO or Entity)")

        # Validate Corporate Name or Hash Number when entity is used in structure
        if not self.corporate_name and not self.hash_number:
            raise ValidationError(
                "Entity in structure must have Corporate Name, Hash Number, or both"
            )

        # Validate share distribution
        if self.owned_entity.total_shares:
            self.validate_shares_distribution()

    def save(self, *args, **kwargs):
        # Auto-calculate percentage from shares (FASE 4)
        if self.owned_shares and self.owned_entity.total_shares:
            calculated_percentage = (self.owned_shares / self.owned_entity.total_shares) * 100
            if not self.ownership_percentage:
                self.ownership_percentage = calculated_percentage

        # Auto-calculate shares from percentage (FASE 4)
        elif self.ownership_percentage and self.owned_entity.total_shares:
            calculated_shares = int((self.ownership_percentage / 100) * self.owned_entity.total_shares)
            if not self.owned_shares:
                self.owned_shares = calculated_shares

        # Calculate total values (FASE 3)
        self.calculate_total_values()

        super().save(*args, **kwargs)

    def calculate_total_values(self):
        """Calculate total values based on shares and share values"""
        if self.share_value_usd and self.owned_shares:
            self.total_value_usd = self.owned_shares * self.share_value_usd
        if self.share_value_eur and self.owned_shares:
            self.total_value_eur = self.owned_shares * self.share_value_eur

    def validate_shares_distribution(self):
        """Validate that all shares have owners (FASE 4)"""
        total_owned = EntityOwnership.objects.filter(
            structure=self.structure,
            owned_entity=self.owned_entity
        ).exclude(pk=self.pk).aggregate(
            total=models.Sum('owned_shares')
        )['total'] or 0

        if self.owned_shares:
            total_owned += self.owned_shares

        if total_owned > self.owned_entity.total_shares:
            raise ValidationError(
                f"Total owned shares ({total_owned}) cannot exceed "
                f"entity total shares ({self.owned_entity.total_shares})"
            )

