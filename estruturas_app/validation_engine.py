"""
SIRIUS Advanced Validation Engine
Comprehensive validation system for legal structure configurations
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime, timedelta

class ValidationLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationCategory(Enum):
    LEGAL = "legal"
    TAX = "tax"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"

@dataclass
class ValidationResult:
    """Individual validation result"""
    level: ValidationLevel
    category: ValidationCategory
    message: str
    description: str
    affected_structures: List[int]
    recommendation: Optional[str] = None
    auto_fixable: bool = False
    priority: int = 1  # 1-5, 5 being highest priority

@dataclass
class ValidationSummary:
    """Complete validation summary"""
    is_valid: bool
    total_issues: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    results: List[ValidationResult]
    overall_score: float  # 0-100, 100 being perfect
    recommendations: List[str]

class SiriusValidationEngine:
    """Advanced validation engine for legal structure configurations"""
    
    def __init__(self):
        # Incompatible structure combinations
        self.incompatible_combinations = {
            ('BDAO_SAC', 'NATIONALIZATION'): "Offshore structures conflict with Brazilian nationalization",
            ('BTS_VAULT', 'WYOMING_FOUNDATION'): "Token structures may conflict with foundation purposes",
            ('FUND_TOKEN', 'NATIONALIZATION'): "Fund tokens incompatible with Brazilian tax residency"
        }
        
        # Required combinations for certain structures
        self.required_combinations = {
            'BDAO_SAC': ['WYOMING_DAO_LLC'],  # BDAO SAC typically requires Wyoming DAO LLC
            'BTS_VAULT': ['WYOMING_CORP'],    # BTS Vault typically requires corporate structure
        }
        
        # Jurisdiction-specific rules
        self.jurisdiction_rules = {
            'US': {
                'max_structures': 5,
                'required_compliance': ['FINCEN', 'IRS'],
                'restricted_combinations': []
            },
            'BAHAMAS': {
                'max_structures': 3,
                'required_compliance': ['BFIU', 'SCB'],
                'restricted_combinations': ['NATIONALIZATION']
            },
            'BRAZIL': {
                'max_structures': 2,
                'required_compliance': ['RFB', 'BACEN'],
                'restricted_combinations': ['BDAO_SAC', 'BTS_VAULT']
            }
        }
        
        # Complexity thresholds
        self.complexity_thresholds = {
            'simple': (1, 2),      # 1-2 complexity score
            'moderate': (3, 3),    # 3 complexity score
            'complex': (4, 4),     # 4 complexity score
            'advanced': (5, 5)     # 5 complexity score
        }
        
        # Cost thresholds for warnings
        self.cost_thresholds = {
            'low': 50000,
            'medium': 100000,
            'high': 250000,
            'extreme': 500000
        }
    
    def validate_configuration(self, 
                             structures: List[Dict], 
                             cost_analysis: Optional[Dict] = None) -> ValidationSummary:
        """Perform comprehensive validation of a legal structure configuration"""
        
        results = []
        
        # Basic structure validation
        results.extend(self._validate_structure_basics(structures))
        
        # Compatibility validation
        results.extend(self._validate_compatibility(structures))
        
        # Jurisdiction validation
        results.extend(self._validate_jurisdictions(structures))
        
        # Complexity validation
        results.extend(self._validate_complexity(structures))
        
        # Cost validation
        if cost_analysis:
            results.extend(self._validate_costs(structures, cost_analysis))
        
        # Strategic validation
        results.extend(self._validate_strategic_alignment(structures))
        
        # Compliance validation
        results.extend(self._validate_compliance_requirements(structures))
        
        # Calculate summary statistics
        summary = self._create_validation_summary(results)
        
        return summary
    
    def _validate_structure_basics(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate basic structure requirements"""
        results = []
        
        if not structures:
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category=ValidationCategory.OPERATIONAL,
                message="No structures selected",
                description="At least one legal structure must be selected to create a valid configuration.",
                affected_structures=[],
                recommendation="Add at least one legal structure to your configuration.",
                priority=5
            ))
            return results
        
        # Check for duplicate structures
        structure_types = [s.get('tipo') for s in structures]
        duplicates = set([t for t in structure_types if structure_types.count(t) > 1])
        
        if duplicates:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message=f"Duplicate structures detected: {', '.join(duplicates)}",
                description="Having multiple instances of the same structure type may create unnecessary complexity.",
                affected_structures=[s.get('id') for s in structures if s.get('tipo') in duplicates],
                recommendation="Consider if multiple instances are truly necessary for your use case.",
                priority=2
            ))
        
        # Check structure count
        if len(structures) > 7:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message="High number of structures",
                description=f"Configuration contains {len(structures)} structures, which may be overly complex.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Consider simplifying the structure to reduce complexity and costs.",
                priority=3
            ))
        
        return results
    
    def _validate_compatibility(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate structure compatibility and required combinations"""
        results = []
        
        structure_types = [s.get('tipo') for s in structures]
        structure_ids = [s.get('id') for s in structures]
        
        # Check for incompatible combinations
        for (type1, type2), message in self.incompatible_combinations.items():
            if type1 in structure_types and type2 in structure_types:
                affected_ids = [s.get('id') for s in structures if s.get('tipo') in [type1, type2]]
                results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category=ValidationCategory.LEGAL,
                    message=f"Incompatible structures: {type1} and {type2}",
                    description=message,
                    affected_structures=affected_ids,
                    recommendation=f"Remove either {type1} or {type2} from the configuration.",
                    priority=5
                ))
        
        # Check for required combinations
        for primary_type, required_types in self.required_combinations.items():
            if primary_type in structure_types:
                missing_required = [rt for rt in required_types if rt not in structure_types]
                if missing_required:
                    primary_id = next(s.get('id') for s in structures if s.get('tipo') == primary_type)
                    results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        category=ValidationCategory.LEGAL,
                        message=f"{primary_type} typically requires {', '.join(missing_required)}",
                        description=f"The {primary_type} structure is most effective when combined with {', '.join(missing_required)}.",
                        affected_structures=[primary_id],
                        recommendation=f"Consider adding {', '.join(missing_required)} to optimize the configuration.",
                        priority=3
                    ))
        
        return results
    
    def _validate_jurisdictions(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate jurisdiction-specific rules and requirements"""
        results = []
        
        # Group structures by jurisdiction
        jurisdiction_groups = {}
        for structure in structures:
            jurisdiction = self._get_structure_jurisdiction(structure.get('tipo'))
            if jurisdiction not in jurisdiction_groups:
                jurisdiction_groups[jurisdiction] = []
            jurisdiction_groups[jurisdiction].append(structure)
        
        # Validate each jurisdiction
        for jurisdiction, jurisdiction_structures in jurisdiction_groups.items():
            rules = self.jurisdiction_rules.get(jurisdiction, {})
            
            # Check maximum structures per jurisdiction
            max_structures = rules.get('max_structures', 10)
            if len(jurisdiction_structures) > max_structures:
                affected_ids = [s.get('id') for s in jurisdiction_structures]
                results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category=ValidationCategory.COMPLIANCE,
                    message=f"Too many structures in {jurisdiction}",
                    description=f"{jurisdiction} has {len(jurisdiction_structures)} structures, exceeding recommended maximum of {max_structures}.",
                    affected_structures=affected_ids,
                    recommendation=f"Consider consolidating or redistributing structures across jurisdictions.",
                    priority=3
                ))
            
            # Check restricted combinations
            restricted = rules.get('restricted_combinations', [])
            for structure in jurisdiction_structures:
                if structure.get('tipo') in restricted:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category=ValidationCategory.LEGAL,
                        message=f"{structure.get('tipo')} restricted in {jurisdiction}",
                        description=f"The {structure.get('tipo')} structure type is not recommended for {jurisdiction} jurisdiction.",
                        affected_structures=[structure.get('id')],
                        recommendation=f"Consider alternative structure types suitable for {jurisdiction}.",
                        priority=4
                    ))
        
        # Multi-jurisdiction complexity warning
        if len(jurisdiction_groups) > 3:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message="High jurisdictional complexity",
                description=f"Configuration spans {len(jurisdiction_groups)} jurisdictions, increasing compliance burden.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Consider consolidating structures in fewer jurisdictions to reduce complexity.",
                priority=2
            ))
        
        return results
    
    def _validate_complexity(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate configuration complexity and provide optimization suggestions"""
        results = []
        
        # Calculate complexity metrics
        total_complexity = sum(s.get('complexidade', 1) for s in structures)
        avg_complexity = total_complexity / len(structures) if structures else 0
        max_complexity = max(s.get('complexidade', 1) for s in structures) if structures else 0
        
        # High average complexity warning
        if avg_complexity > 3.5:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message="High average complexity",
                description=f"Configuration has average complexity of {avg_complexity:.1f}, which may require specialized expertise.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Ensure adequate legal and operational expertise is available for implementation.",
                priority=3
            ))
        
        # Maximum complexity warning
        if max_complexity >= 5:
            high_complexity_structures = [s for s in structures if s.get('complexidade', 1) >= 5]
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message="Extremely complex structures present",
                description="Configuration includes structures with maximum complexity rating.",
                affected_structures=[s.get('id') for s in high_complexity_structures],
                recommendation="Consider phased implementation and specialized legal counsel for complex structures.",
                priority=4
            ))
        
        return results
    
    def _validate_costs(self, structures: List[Dict], cost_analysis: Dict) -> List[ValidationResult]:
        """Validate cost-related aspects of the configuration"""
        results = []
        
        total_cost = cost_analysis.get('risk_adjusted_cost', 0)
        setup_cost = cost_analysis.get('total_setup_cost', 0)
        annual_cost = cost_analysis.get('total_annual_cost', 0)
        
        # High cost warnings
        if total_cost > self.cost_thresholds['extreme']:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.STRATEGIC,
                message="Extremely high configuration cost",
                description=f"Total cost of ${total_cost:,.2f} is exceptionally high.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Consider phased implementation or alternative structure combinations to reduce costs.",
                priority=4
            ))
        elif total_cost > self.cost_thresholds['high']:
            results.append(ValidationResult(
                level=ValidationLevel.INFO,
                category=ValidationCategory.STRATEGIC,
                message="High configuration cost",
                description=f"Total cost of ${total_cost:,.2f} requires significant investment.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Ensure budget allocation and consider cost-benefit analysis.",
                priority=2
            ))
        
        # High annual maintenance cost
        if annual_cost > setup_cost * 0.3:  # Annual cost > 30% of setup cost
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.OPERATIONAL,
                message="High annual maintenance costs",
                description=f"Annual maintenance of ${annual_cost:,.2f} is {(annual_cost/setup_cost)*100:.1f}% of setup costs.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Consider structures with lower ongoing maintenance requirements.",
                priority=3
            ))
        
        # Cost-benefit analysis
        risk_analysis = cost_analysis.get('risk_analysis', {})
        if risk_analysis.get('overall_risk_level') == 'high' and total_cost > self.cost_thresholds['medium']:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.STRATEGIC,
                message="High cost with high risk",
                description="Configuration combines high costs with elevated risk levels.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Consider risk mitigation strategies or alternative approaches.",
                priority=4
            ))
        
        return results
    
    def _validate_strategic_alignment(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate strategic alignment and purpose coherence"""
        results = []
        
        # Analyze structure purposes and alignment
        structure_purposes = self._categorize_structure_purposes(structures)
        
        # Check for conflicting purposes
        if len(structure_purposes) > 3:
            results.append(ValidationResult(
                level=ValidationLevel.INFO,
                category=ValidationCategory.STRATEGIC,
                message="Diverse strategic purposes",
                description=f"Configuration serves {len(structure_purposes)} different strategic purposes.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Ensure all structures align with overall strategic objectives.",
                priority=1
            ))
        
        # Check for redundant structures
        redundancy_check = self._check_structural_redundancy(structures)
        if redundancy_check:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.STRATEGIC,
                message="Potential structural redundancy",
                description="Some structures may serve overlapping purposes.",
                affected_structures=redundancy_check,
                recommendation="Review structure purposes to eliminate redundancy.",
                priority=2
            ))
        
        return results
    
    def _validate_compliance_requirements(self, structures: List[Dict]) -> List[ValidationResult]:
        """Validate compliance requirements and regulatory considerations"""
        results = []
        
        # Check for high-compliance structures
        high_compliance_structures = [
            s for s in structures 
            if s.get('tipo') in ['BDAO_SAC', 'BTS_VAULT', 'FUND_TOKEN']
        ]
        
        if high_compliance_structures:
            results.append(ValidationResult(
                level=ValidationLevel.INFO,
                category=ValidationCategory.COMPLIANCE,
                message="High-compliance structures detected",
                description="Configuration includes structures with elevated regulatory requirements.",
                affected_structures=[s.get('id') for s in high_compliance_structures],
                recommendation="Ensure compliance expertise and ongoing monitoring capabilities.",
                priority=3
            ))
        
        # Check implementation timeline vs compliance requirements
        max_implementation_time = max(s.get('tempo_implementacao', 30) for s in structures)
        if max_implementation_time > 120:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category=ValidationCategory.COMPLIANCE,
                message="Extended implementation timeline",
                description=f"Implementation may take up to {max_implementation_time} days.",
                affected_structures=[s.get('id') for s in structures],
                recommendation="Plan for regulatory changes during extended implementation period.",
                priority=2
            ))
        
        return results
    
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
    
    def _categorize_structure_purposes(self, structures: List[Dict]) -> Set[str]:
        """Categorize structures by their primary purposes"""
        purpose_map = {
            'BDAO_SAC': 'asset_protection',
            'WYOMING_DAO_LLC': 'operational',
            'WYOMING_FOUNDATION': 'succession_planning',
            'WYOMING_CORP': 'operational',
            'BTS_VAULT': 'tokenization',
            'NATIONALIZATION': 'tax_optimization',
            'FUND_TOKEN': 'investment_vehicle'
        }
        
        purposes = set()
        for structure in structures:
            purpose = purpose_map.get(structure.get('tipo'), 'general')
            purposes.add(purpose)
        
        return purposes
    
    def _check_structural_redundancy(self, structures: List[Dict]) -> List[int]:
        """Check for potentially redundant structures"""
        redundant_ids = []
        
        # Check for multiple operational structures
        operational_structures = [
            s for s in structures 
            if s.get('tipo') in ['WYOMING_DAO_LLC', 'WYOMING_CORP']
        ]
        
        if len(operational_structures) > 2:
            redundant_ids.extend([s.get('id') for s in operational_structures[2:]])
        
        return redundant_ids
    
    def _create_validation_summary(self, results: List[ValidationResult]) -> ValidationSummary:
        """Create comprehensive validation summary"""
        
        # Count results by level
        level_counts = {level: 0 for level in ValidationLevel}
        for result in results:
            level_counts[result.level] += 1
        
        # Determine overall validity
        is_valid = level_counts[ValidationLevel.CRITICAL] == 0 and level_counts[ValidationLevel.ERROR] == 0
        
        # Calculate overall score (0-100)
        total_issues = len(results)
        if total_issues == 0:
            overall_score = 100.0
        else:
            # Weight different issue types
            weighted_score = (
                level_counts[ValidationLevel.CRITICAL] * 25 +
                level_counts[ValidationLevel.ERROR] * 15 +
                level_counts[ValidationLevel.WARNING] * 8 +
                level_counts[ValidationLevel.INFO] * 2
            )
            overall_score = max(0, 100 - weighted_score)
        
        # Generate high-level recommendations
        recommendations = self._generate_summary_recommendations(results, level_counts)
        
        return ValidationSummary(
            is_valid=is_valid,
            total_issues=total_issues,
            critical_count=level_counts[ValidationLevel.CRITICAL],
            error_count=level_counts[ValidationLevel.ERROR],
            warning_count=level_counts[ValidationLevel.WARNING],
            info_count=level_counts[ValidationLevel.INFO],
            results=sorted(results, key=lambda r: (r.priority, r.level.value), reverse=True),
            overall_score=overall_score,
            recommendations=recommendations
        )
    
    def _generate_summary_recommendations(self, 
                                        results: List[ValidationResult], 
                                        level_counts: Dict[ValidationLevel, int]) -> List[str]:
        """Generate high-level recommendations based on validation results"""
        
        recommendations = []
        
        if level_counts[ValidationLevel.CRITICAL] > 0:
            recommendations.append("Address critical issues immediately before proceeding")
        
        if level_counts[ValidationLevel.ERROR] > 0:
            recommendations.append("Resolve all errors to ensure legal compliance")
        
        if level_counts[ValidationLevel.WARNING] > 3:
            recommendations.append("Consider simplifying configuration to reduce warnings")
        
        # Category-specific recommendations
        categories = [r.category for r in results]
        if categories.count(ValidationCategory.LEGAL) > 2:
            recommendations.append("Seek specialized legal counsel for complex legal issues")
        
        if categories.count(ValidationCategory.COMPLIANCE) > 2:
            recommendations.append("Establish robust compliance monitoring procedures")
        
        if categories.count(ValidationCategory.OPERATIONAL) > 3:
            recommendations.append("Develop comprehensive operational procedures")
        
        return recommendations

# Django integration function
def validate_configuration_django(structures_data: List[Dict], 
                                cost_analysis: Optional[Dict] = None) -> Dict:
    """Django-compatible wrapper for configuration validation"""
    
    validator = SiriusValidationEngine()
    summary = validator.validate_configuration(structures_data, cost_analysis)
    
    # Convert to JSON-serializable format
    return {
        'is_valid': summary.is_valid,
        'total_issues': summary.total_issues,
        'critical_count': summary.critical_count,
        'error_count': summary.error_count,
        'warning_count': summary.warning_count,
        'info_count': summary.info_count,
        'overall_score': summary.overall_score,
        'recommendations': summary.recommendations,
        'results': [
            {
                'level': result.level.value,
                'category': result.category.value,
                'message': result.message,
                'description': result.description,
                'affected_structures': result.affected_structures,
                'recommendation': result.recommendation,
                'auto_fixable': result.auto_fixable,
                'priority': result.priority
            }
            for result in summary.results
        ]
    }

