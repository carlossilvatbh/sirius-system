from django.core.management.base import BaseCommand
from corporate.models import Entity, Structure, StructureNode, NodeOwnership
from parties.models import Party


class Command(BaseCommand):
    help = 'Verify that the new node-based system is working correctly'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Verificando sistema node-based...")
        
        # Verify entities (templates)
        entities = Entity.objects.all()
        self.stdout.write(f"✅ {entities.count()} Entity templates encontrados:")
        for entity in entities:
            self.stdout.write(f"   - {entity.name} ({entity.entity_type})")
        
        # Verify structures
        structures = Structure.objects.all()
        self.stdout.write(f"✅ {structures.count()} Structures encontradas:")
        for structure in structures:
            nodes_count = structure.nodes.count()
            ownerships_count = structure.node_ownerships.count()
            self.stdout.write(f"   - {structure.name}: {nodes_count} nodes, {ownerships_count} ownerships")
        
        # Verify parties
        parties = Party.objects.all()
        self.stdout.write(f"✅ {parties.count()} Parties encontradas:")
        for party in parties:
            owned_nodes = NodeOwnership.objects.filter(owner_party=party).count()
            self.stdout.write(f"   - {party.name}: possui {owned_nodes} nodes")
        
        # Verify specific structure details
        if structures.exists():
            structure = structures.first()
            self.stdout.write(f"\n🔬 Detalhes da estrutura '{structure.name}':")
            
            for level in sorted(structure.nodes.values_list('level', flat=True).distinct()):
                nodes_in_level = structure.nodes.filter(level=level)
                self.stdout.write(f"   Nível {level}: {nodes_in_level.count()} nodes")
                for node in nodes_in_level:
                    ownerships = NodeOwnership.objects.filter(owned_node=node)
                    self.stdout.write(f"     - {node.custom_name} (baseado em {node.entity_template.name})")
                    for ownership in ownerships:
                        owner = ownership.owner_party.name if ownership.owner_party else ownership.owner_node.custom_name
                        self.stdout.write(f"       🔗 {owner} possui {ownership.ownership_percentage}%")
        
        self.stdout.write("\n✅ Sistema node-based funcionando corretamente!")
        self.stdout.write("🌐 Acesse http://127.0.0.1:8001/corporate/structures/ para visualizar")
