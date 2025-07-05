"""
SIRIUS Advanced Cost Calculator
Comprehensive cost calculation system with scenario modeling and risk analysis
"""

import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class CostScenario(Enum):
    BASIC = "basic"
    COMPLETE = "complete"
    PREMIUM = "premium"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CostComponent:
    """Individual cost component with detailed breakdown"""
    name: str
    base_amount: Decimal
    category: str  # setup, maintenance, legal, compliance, tax
    frequency: str  # one_time, monthly, quarterly, annual
    risk_factor: float = 1.0
    complexity_multiplier: float = 1.0
    jurisdiction_factor: float = 1.0

@dataclass
class StructureCostAnalysis:
    """Detailed cost analysis for a single structure"""
    structure_id: int
    base_cost: Decimal
    components: List[CostComponent]
    total_setup_cost: Decimal
    annual_maintenance: Decimal
    complexity_score: int
    risk_level: RiskLevel
    implementation_time: int
    dependencies: List[int] = None

@dataclass
class ConfigurationCostResult:
    """Complete cost analysis result for a configuration"""
    total_setup_cost: Decimal
    total_annual_cost: Decimal
    scenario_adjusted_cost: Decimal
    risk_adjusted_cost: Decimal
    complexity_bonus: Decimal
    jurisdiction_penalties: Decimal
    time_to_implementation: int
    cost_breakdown: Dict[str, Decimal]
    risk_analysis: Dict[str, any]
    recommendations: List[str]

class SiriusCostCalculator:
    """Advanced cost calculator with scenario modeling and risk analysis"""
    
    def __init__(self):
        self.scenario_multipliers = {
            CostScenario.BASIC: 1.0,
            CostScenario.COMPLETE: 1.5,
            CostScenario.PREMIUM: 2.2
        }
        
        self.risk_multipliers = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 1.15,
            RiskLevel.HIGH: 1.35,
            RiskLevel.CRITICAL: 1.65
        }
        
        self.complexity_discounts = {
            1: 0.0,   # No discount for simple structures
            2: 0.02,  # 2% discount for moderate complexity
            3: 0.05,  # 5% discount for complex structures
            4: 0.08,  # 8% discount for very complex
            5: 0.12   # 12% discount for extremely complex
        }
        
        self.jurisdiction_factors = {
            'US': 1.0,
            'BAHAMAS': 1.1,
            'BRAZIL': 1.25,
            'CAYMAN': 0.95,
            'SINGAPORE': 1.05,
            'SWITZERLAND': 1.3
        }
    
    def calculate_structure_costs(self, structure_data: Dict) -> StructureCostAnalysis:
        """Calculate detailed costs for a single structure"""
        
        # Extract structure information
        structure_id = structure_data.get('id')
        base_cost = Decimal(str(structure_data.get('custo_base', 0)))
        maintenance_cost = Decimal(str(structure_data.get('custo_manutencao', 0)))
        complexity = structure_data.get('complexidade', 1)
        implementation_time = structure_data.get('tempo_implementacao', 30)
        
        # Determine risk level based on structure type and complexity
        risk_level = self._assess_risk_level(structure_data)
        
        # Create detailed cost components
        components = self._create_cost_components(structure_data)
        
        # Calculate total costs
        total_setup = self._calculate_total_setup_cost(components, complexity)
        annual_maintenance = self._calculate_annual_maintenance(components, maintenance_cost)
        
        return StructureCostAnalysis(
            structure_id=structure_id,
            base_cost=base_cost,
            components=components,
            total_setup_cost=total_setup,
            annual_maintenance=annual_maintenance,
            complexity_score=complexity,
            risk_level=risk_level,
            implementation_time=implementation_time,
            dependencies=structure_data.get('dependencies', [])
        )
    
    def calculate_configuration_cost(self, 
                                   structures: List[Dict], 
                                   scenario: CostScenario = CostScenario.BASIC,
                                   include_risk_analysis: bool = True) -> ConfigurationCostResult:
        """Calculate comprehensive costs for entire configuration"""
        
        # Analyze each structure
        structure_analyses = []
        for structure in structures:
            analysis = self.calculate_structure_costs(structure)
            structure_analyses.append(analysis)
        
        # Calculate base totals
        total_setup = sum(analysis.total_setup_cost for analysis in structure_analyses)
        total_annual = sum(analysis.annual_maintenance for analysis in structure_analyses)
        
        # Apply scenario multiplier
        scenario_multiplier = self.scenario_multipliers[scenario]
        scenario_adjusted = total_setup * Decimal(str(scenario_multiplier))
        
        # Calculate complexity bonus (discount for complex configurations)
        complexity_bonus = self._calculate_complexity_bonus(structure_analyses)
        
        # Calculate jurisdiction penalties
        jurisdiction_penalties = self._calculate_jurisdiction_penalties(structures)
        
        # Apply risk adjustments if requested
        risk_adjusted_cost = scenario_adjusted
        risk_analysis = {}
        
        if include_risk_analysis:
            risk_analysis = self._perform_risk_analysis(structure_analyses)
            risk_multiplier = risk_analysis.get('overall_risk_multiplier', 1.0)
            risk_adjusted_cost = scenario_adjusted * Decimal(str(risk_multiplier))
        
        # Calculate implementation time (critical path)
        implementation_time = self._calculate_implementation_time(structure_analyses)
        
        # Create cost breakdown
        cost_breakdown = {
            'setup_costs': total_setup,
            'annual_maintenance': total_annual,
            'scenario_adjustment': scenario_adjusted - total_setup,
            'complexity_bonus': complexity_bonus,
            'jurisdiction_penalties': jurisdiction_penalties,
            'risk_adjustment': risk_adjusted_cost - scenario_adjusted if include_risk_analysis else Decimal('0')
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(structure_analyses, risk_analysis)
        
        # Final cost calculation
        final_cost = risk_adjusted_cost - complexity_bonus + jurisdiction_penalties
        
        return ConfigurationCostResult(
            total_setup_cost=total_setup,
            total_annual_cost=total_annual,
            scenario_adjusted_cost=scenario_adjusted,
            risk_adjusted_cost=final_cost,
            complexity_bonus=complexity_bonus,
            jurisdiction_penalties=jurisdiction_penalties,
            time_to_implementation=implementation_time,
            cost_breakdown=cost_breakdown,
            risk_analysis=risk_analysis,
            recommendations=recommendations
        )
    
    def _assess_risk_level(self, structure_data: Dict) -> RiskLevel:
        """Assess risk level based on structure characteristics"""
        
        structure_type = structure_data.get('tipo', '')
        complexity = structure_data.get('complexidade', 1)
        confidentiality = structure_data.get('nivel_confidencialidade', 1)
        
        # Risk scoring algorithm
        risk_score = 0
        
        # Type-based risk
        high_risk_types = ['BDAO_SAC', 'BTS_VAULT', 'FUND_TOKEN']
        medium_risk_types = ['WYOMING_DAO_LLC', 'WYOMING_FOUNDATION']
        
        if structure_type in high_risk_types:
            risk_score += 3
        elif structure_type in medium_risk_types:
            risk_score += 2
        else:
            risk_score += 1
        
        # Complexity risk
        risk_score += complexity - 1
        
        # Confidentiality risk
        risk_score += max(0, confidentiality - 3)
        
        # Determine risk level
        if risk_score <= 3:
            return RiskLevel.LOW
        elif risk_score <= 6:
            return RiskLevel.MEDIUM
        elif risk_score <= 9:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _create_cost_components(self, structure_data: Dict) -> List[CostComponent]:
        """Create detailed cost components for a structure"""
        
        base_cost = Decimal(str(structure_data.get('custo_base', 0)))
        maintenance_cost = Decimal(str(structure_data.get('custo_manutencao', 0)))
        complexity = structure_data.get('complexidade', 1)
        
        components = []
        
        # Setup costs
        components.append(CostComponent(
            name="Legal Structure Setup",
            base_amount=base_cost * Decimal('0.6'),
            category="setup",
            frequency="one_time",
            complexity_multiplier=1.0 + (complexity - 1) * 0.1
        ))
        
        components.append(CostComponent(
            name="Legal Documentation",
            base_amount=base_cost * Decimal('0.25'),
            category="legal",
            frequency="one_time",
            complexity_multiplier=1.0 + (complexity - 1) * 0.15
        ))
        
        components.append(CostComponent(
            name="Compliance Setup",
            base_amount=base_cost * Decimal('0.15'),
            category="compliance",
            frequency="one_time",
            complexity_multiplier=1.0 + (complexity - 1) * 0.2
        ))
        
        # Maintenance costs
        components.append(CostComponent(
            name="Annual Compliance",
            base_amount=maintenance_cost * Decimal('0.7'),
            category="compliance",
            frequency="annual",
            complexity_multiplier=1.0 + (complexity - 1) * 0.1
        ))
        
        components.append(CostComponent(
            name="Legal Maintenance",
            base_amount=maintenance_cost * Decimal('0.3'),
            category="legal",
            frequency="annual",
            complexity_multiplier=1.0 + (complexity - 1) * 0.05
        ))
        
        return components
    
    def _calculate_total_setup_cost(self, components: List[CostComponent], complexity: int) -> Decimal:
        """Calculate total setup cost with complexity adjustments"""
        
        setup_components = [c for c in components if c.frequency == "one_time"]
        total = Decimal('0')
        
        for component in setup_components:
            adjusted_amount = component.base_amount * Decimal(str(component.complexity_multiplier))
            total += adjusted_amount
        
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _calculate_annual_maintenance(self, components: List[CostComponent], base_maintenance: Decimal) -> Decimal:
        """Calculate annual maintenance cost"""
        
        annual_components = [c for c in components if c.frequency == "annual"]
        total = Decimal('0')
        
        for component in annual_components:
            adjusted_amount = component.base_amount * Decimal(str(component.complexity_multiplier))
            total += adjusted_amount
        
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _calculate_complexity_bonus(self, analyses: List[StructureCostAnalysis]) -> Decimal:
        """Calculate complexity bonus (discount for sophisticated configurations)"""
        
        if not analyses:
            return Decimal('0')
        
        # Calculate average complexity
        avg_complexity = sum(a.complexity_score for a in analyses) / len(analyses)
        
        # Calculate total setup cost
        total_setup = sum(a.total_setup_cost for a in analyses)
        
        # Apply complexity discount
        discount_rate = self.complexity_discounts.get(int(avg_complexity), 0)
        bonus = total_setup * Decimal(str(discount_rate))
        
        return bonus.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _calculate_jurisdiction_penalties(self, structures: List[Dict]) -> Decimal:
        """Calculate jurisdiction-based cost adjustments"""
        
        penalties = Decimal('0')
        
        for structure in structures:
            # Determine jurisdiction based on structure type
            jurisdiction = self._get_structure_jurisdiction(structure.get('tipo', ''))
            factor = self.jurisdiction_factors.get(jurisdiction, 1.0)
            
            if factor > 1.0:
                base_cost = Decimal(str(structure.get('custo_base', 0)))
                penalty = base_cost * Decimal(str(factor - 1.0))
                penalties += penalty
        
        return penalties.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _get_structure_jurisdiction(self, structure_type: str) -> str:
        """Determine jurisdiction based on structure type"""
        
        jurisdiction_map = {
            'BDAO_SAC': 'BAHAMAS',
            'WYOMING_DAO_LLC': 'US',
            'WYOMING_FOUNDATION': 'US',
            'WYOMING_CORP': 'US',
            'BTS_VAULT': 'US',
            'NATIONALIZATION': 'BRAZIL',
            'FUND_TOKEN': 'US'
        }
        
        return jurisdiction_map.get(structure_type, 'US')
    
    def _perform_risk_analysis(self, analyses: List[StructureCostAnalysis]) -> Dict:
        """Perform comprehensive risk analysis"""
        
        if not analyses:
            return {'overall_risk_multiplier': 1.0}
        
        # Calculate risk distribution
        risk_counts = {level: 0 for level in RiskLevel}
        for analysis in analyses:
            risk_counts[analysis.risk_level] += 1
        
        # Calculate weighted risk score
        risk_weights = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
        
        total_weight = sum(risk_weights[level] * count for level, count in risk_counts.items())
        avg_risk_weight = total_weight / len(analyses)
        
        # Determine overall risk multiplier
        if avg_risk_weight <= 1.5:
            overall_risk = RiskLevel.LOW
        elif avg_risk_weight <= 2.5:
            overall_risk = RiskLevel.MEDIUM
        elif avg_risk_weight <= 3.5:
            overall_risk = RiskLevel.HIGH
        else:
            overall_risk = RiskLevel.CRITICAL
        
        risk_multiplier = self.risk_multipliers[overall_risk]
        
        return {
            'overall_risk_level': overall_risk.value,
            'overall_risk_multiplier': risk_multiplier,
            'risk_distribution': {level.value: count for level, count in risk_counts.items()},
            'average_risk_score': avg_risk_weight,
            'risk_factors': self._identify_risk_factors(analyses)
        }
    
    def _identify_risk_factors(self, analyses: List[StructureCostAnalysis]) -> List[str]:
        """Identify specific risk factors in the configuration"""
        
        factors = []
        
        # Check for high-risk structures
        high_risk_count = sum(1 for a in analyses if a.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL])
        if high_risk_count > 0:
            factors.append(f"{high_risk_count} high-risk structure(s) detected")
        
        # Check for complexity issues
        high_complexity_count = sum(1 for a in analyses if a.complexity_score >= 4)
        if high_complexity_count > 0:
            factors.append(f"{high_complexity_count} highly complex structure(s)")
        
        # Check for implementation time
        max_implementation = max(a.implementation_time for a in analyses)
        if max_implementation > 90:
            factors.append(f"Extended implementation timeline ({max_implementation} days)")
        
        # Check for jurisdiction diversity
        jurisdictions = set(self._get_structure_jurisdiction(a.structure_id) for a in analyses)
        if len(jurisdictions) > 2:
            factors.append(f"Multiple jurisdictions involved ({len(jurisdictions)})")
        
        return factors
    
    def _calculate_implementation_time(self, analyses: List[StructureCostAnalysis]) -> int:
        """Calculate critical path implementation time"""
        
        if not analyses:
            return 0
        
        # For now, use maximum implementation time
        # In a more sophisticated version, this would consider dependencies
        return max(a.implementation_time for a in analyses)
    
    def _generate_recommendations(self, 
                                analyses: List[StructureCostAnalysis], 
                                risk_analysis: Dict) -> List[str]:
        """Generate cost optimization and risk mitigation recommendations"""
        
        recommendations = []
        
        if not analyses:
            return recommendations
        
        # Cost optimization recommendations
        total_cost = sum(a.total_setup_cost for a in analyses)
        if total_cost > Decimal('100000'):
            recommendations.append("Consider phased implementation to spread costs over time")
        
        # Risk mitigation recommendations
        overall_risk = risk_analysis.get('overall_risk_level', 'low')
        if overall_risk in ['high', 'critical']:
            recommendations.append("High-risk configuration detected - consider additional legal review")
        
        # Complexity recommendations
        high_complexity_count = sum(1 for a in analyses if a.complexity_score >= 4)
        if high_complexity_count > 1:
            recommendations.append("Multiple complex structures - ensure adequate project management")
        
        # Implementation time recommendations
        max_time = max(a.implementation_time for a in analyses)
        if max_time > 120:
            recommendations.append("Extended timeline - consider parallel implementation where possible")
        
        # Jurisdiction recommendations
        jurisdictions = set(self._get_structure_jurisdiction(str(a.structure_id)) for a in analyses)
        if len(jurisdictions) > 2:
            recommendations.append("Multiple jurisdictions - coordinate with local legal experts")
        
        return recommendations

# Utility functions for Django integration
def calculate_configuration_cost_django(elementos_data: List[Dict], 
                                       scenario: str = 'basic',
                                       include_risk: bool = True) -> Dict:
    """Django-compatible wrapper for cost calculation"""
    
    calculator = SiriusCostCalculator()
    
    # Convert scenario string to enum
    scenario_map = {
        'basic': CostScenario.BASIC,
        'complete': CostScenario.COMPLETE,
        'premium': CostScenario.PREMIUM
    }
    scenario_enum = scenario_map.get(scenario, CostScenario.BASIC)
    
    # Calculate costs
    result = calculator.calculate_configuration_cost(
        elementos_data, 
        scenario_enum, 
        include_risk
    )
    
    # Convert to JSON-serializable format
    return {
        'total_setup_cost': float(result.total_setup_cost),
        'total_annual_cost': float(result.total_annual_cost),
        'scenario_adjusted_cost': float(result.scenario_adjusted_cost),
        'risk_adjusted_cost': float(result.risk_adjusted_cost),
        'complexity_bonus': float(result.complexity_bonus),
        'jurisdiction_penalties': float(result.jurisdiction_penalties),
        'time_to_implementation': result.time_to_implementation,
        'cost_breakdown': {k: float(v) for k, v in result.cost_breakdown.items()},
        'risk_analysis': result.risk_analysis,
        'recommendations': result.recommendations
    }

