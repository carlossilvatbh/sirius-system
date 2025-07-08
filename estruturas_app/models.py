from corporate.models import Structure


class Estrutura(Structure):
    """
    Proxy model for backward compatibility.
    This model inherits all functionality from corporate.Structure
    but maintains the original name for legacy code compatibility.
    
    DEPRECATED: Use corporate.Structure directly in new code.
    """
    
    class Meta:
        proxy = True
        verbose_name = "Legal Structure (Legacy)"
        verbose_name_plural = "Legal Structures (Legacy)"
