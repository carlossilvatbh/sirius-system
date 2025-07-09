from django.core.management.base import BaseCommand
from django.db import transaction
from corporate.models import Entity, Structure, StructureNode, NodeOwnership
from parties.models import Party


class Command(BaseCommand):
    help = 'Populate database with example entities and structures following the new node-based system'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Creating example entities and structures...")
            
            # Create the Entity templates (reusable entities)
            wyoming_llc = self.create_wyoming_dao_llc()
            bahamas_fund = self.create_bahamas_fund()
            
            # Create a sample party (UBO)
            party = self.create_sample_party()
            
            # Create an example structure
            structure = self.create_example_structure(wyoming_llc, bahamas_fund, party)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created:\n'
                    f'- Entity templates: {wyoming_llc.name}, {bahamas_fund.name}\n'
                    f'- Party: {party.name}\n'
                    f'- Structure: {structure.name} with {structure.nodes.count()} nodes'
                )
            )

    def create_wyoming_dao_llc(self):
        """Create Wyoming DAO LLC entity template"""
        entity, created = Entity.objects.get_or_create(
            name="Wyoming DAO LLC",
            defaults={
                'entity_type': 'LLC_DISREGARDED',
                'tax_classification': 'LLC_DISREGARDED_ENTITY',
                'implementation_documents': {
                    'operating_agreement': 'docs.google.com/oa.docx',
                    'memorandum': 'docs.google.com/memorandum.docx'
                },
                'jurisdiction': 'US',
                'us_state': 'WY',
                'implementation_time': 1,
                'tax_impact_usa': 'tributa a camada superior',
                'tax_impact_brazil': 'indeterminado',
                'tax_impact_local': 'indeterminado',
                'confidentiality_level': 5,
                'asset_protection': 5,
                'privacy_impact': 'privacidade nos termos da lei',
                'banking_facility': 5,
                'required_documents': 'Passaporte\nProof of address',
                'legal_requirements': 'Obrigações legais conforme jurisdição Wyoming',
                'active': True
            }
        )
        
        if created:
            self.stdout.write(f"✅ Created Wyoming DAO LLC entity template")
        else:
            self.stdout.write(f"⚠️ Wyoming DAO LLC already exists")
            
        return entity

    def create_bahamas_fund(self):
        """Create Bahamas Fund entity template"""
        entity, created = Entity.objects.get_or_create(
            name="Bahamas Fund",
            defaults={
                'entity_type': 'FUND',
                'tax_classification': 'FUND',
                'implementation_documents': {
                    'operating_agreement': 'docs.google.com/oa.docx',
                    'memorandum': 'docs.google.com/memorandum.docx'
                },
                'jurisdiction': 'BS',
                'us_state': None,
                'implementation_time': 1,
                'tax_impact_usa': 'não tem tributação',
                'tax_impact_brazil': 'indeterminado',
                'tax_impact_local': 'indeterminado',
                'confidentiality_level': 5,
                'asset_protection': 5,
                'privacy_impact': 'privacidade nos termos da lei',
                'banking_facility': 5,
                'required_documents': 'Passaporte\nProof of address',
                'legal_requirements': 'Obrigações legais conforme jurisdição Bahamas',
                'active': True
            }
        )
        
        if created:
            self.stdout.write(f"✅ Created Bahamas Fund entity template")
        else:
            self.stdout.write(f"⚠️ Bahamas Fund already exists")
            
        return entity

    def create_sample_party(self):
        """Create a sample party (UBO)"""
        party, created = Party.objects.get_or_create(
            name="João da Silva",
            defaults={
                'person_type': 'NATURAL_PERSON',
                'tax_identification_number': '123.456.789-00',
                'email': 'joao@example.com',
                'nationality': 'BR',
                'active': True
            }
        )
        
        if created:
            self.stdout.write(f"✅ Created sample party: {party.name}")
        else:
            self.stdout.write(f"⚠️ Party {party.name} already exists")
            
        return party

    def create_example_structure(self, wyoming_llc, bahamas_fund, party):
        """Create an example 4-level structure"""
        
        # Create the structure
        structure, created = Structure.objects.get_or_create(
            name="Exemplo Multi-Nível Structure",
            defaults={
                'description': 'Estrutura de exemplo com 4 níveis usando Wyoming LLC e Bahamas Fund',
                'status': 'DRAFTING'
            }
        )
        
        if created:
            self.stdout.write(f"✅ Created structure: {structure.name}")
        else:
            self.stdout.write(f"⚠️ Structure {structure.name} already exists, clearing nodes...")
            # Clear existing nodes to recreate
            structure.nodes.all().delete()
        
        # Level 1 (Top level) - 2 nodes
        level1_node1 = StructureNode.objects.create(
            structure=structure,
            entity_template=wyoming_llc,
            custom_name="João's Primary Wyoming LLC",
            total_shares=1000,
            corporate_name="João Primary LLC Corp",
            hash_number="WY001",
            level=1,
            parent_node=None,
            is_active=True
        )
        
        level1_node2 = StructureNode.objects.create(
            structure=structure,
            entity_template=bahamas_fund,
            custom_name="Investment Fund Level 1",
            total_shares=500,
            corporate_name="Level1 Investment Fund Corp",
            hash_number="BS001",
            level=1,
            parent_node=None,
            is_active=True
        )
        
        # Level 2 - Children of Level 1 nodes
        level2_node1 = StructureNode.objects.create(
            structure=structure,
            entity_template=wyoming_llc,
            custom_name="Secondary Wyoming LLC",
            total_shares=800,
            corporate_name="Secondary LLC Corp",
            hash_number="WY002",
            level=2,
            parent_node=level1_node1,
            is_active=True
        )
        
        level2_node2 = StructureNode.objects.create(
            structure=structure,
            entity_template=bahamas_fund,
            custom_name="Investment Fund Level 2",
            total_shares=300,
            corporate_name="Level2 Investment Fund Corp",
            hash_number="BS002",
            level=2,
            parent_node=level1_node2,
            is_active=True
        )
        
        # Level 3
        level3_node1 = StructureNode.objects.create(
            structure=structure,
            entity_template=wyoming_llc,
            custom_name="Tertiary Wyoming LLC",
            total_shares=600,
            corporate_name="Tertiary LLC Corp",
            hash_number="WY003",
            level=3,
            parent_node=level2_node1,
            is_active=True
        )
        
        # Level 4
        level4_node1 = StructureNode.objects.create(
            structure=structure,
            entity_template=bahamas_fund,
            custom_name="Final Investment Fund",
            total_shares=200,
            corporate_name="Final Investment Fund Corp",
            hash_number="BS003",
            level=4,
            parent_node=level3_node1,
            is_active=True
        )
        
        # Create ownership relationships
        
        # Party owns Level 1 nodes
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=party,
            owner_node=None,
            owned_node=level1_node1,
            ownership_percentage=70.00,
            owned_shares=700,
            share_value_usd=100.00
        )
        
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=party,
            owner_node=None,
            owned_node=level1_node2,
            ownership_percentage=100.00,
            owned_shares=500,
            share_value_usd=200.00
        )
        
        # Level 1 nodes own Level 2 nodes
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=None,
            owner_node=level1_node1,
            owned_node=level2_node1,
            ownership_percentage=85.00,
            owned_shares=680,
            share_value_usd=150.00
        )
        
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=None,
            owner_node=level1_node2,
            owned_node=level2_node2,
            ownership_percentage=90.00,
            owned_shares=270,
            share_value_usd=250.00
        )
        
        # Level 2 node owns Level 3 node
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=None,
            owner_node=level2_node1,
            owned_node=level3_node1,
            ownership_percentage=95.00,
            owned_shares=570,
            share_value_usd=180.00
        )
        
        # Level 3 node owns Level 4 node
        NodeOwnership.objects.create(
            structure=structure,
            owner_party=None,
            owner_node=level3_node1,
            owned_node=level4_node1,
            ownership_percentage=100.00,
            owned_shares=200,
            share_value_usd=300.00
        )
        
        self.stdout.write(f"✅ Created {structure.nodes.count()} nodes and {structure.node_ownerships.count()} ownership relationships")
        
        return structure
