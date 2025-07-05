from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
import logging

from .models import Estrutura, RegraValidacao, Template, ConfiguracaoSalva, AlertaJurisdicao

logger = logging.getLogger(__name__)


def canvas_principal(request):
    """
    Main canvas page for the SIRIUS system.
    Displays the drag-and-drop interface with available structures and templates.
    """
    estruturas = Estrutura.objects.filter(ativo=True).order_by('nome')
    templates = Template.objects.filter(ativo=True).order_by('-uso_count')[:10]
    
    # Get jurisdiction alerts for display
    alertas = AlertaJurisdicao.objects.filter(ativo=True, prioridade__gte=3).order_by('-prioridade')[:5]
    
    context = {
        'estruturas': estruturas,
        'templates': templates,
        'alertas': alertas,
        'page_title': 'SIRIUS - Legal Structure Canvas'
    }
    
    return render(request, 'canvas_vue.html', context)


def estruturas_json(request):
    """
    API endpoint returning all active structures with complete information.
    Used by the frontend to populate the structure library.
    """
    try:
        estruturas = Estrutura.objects.filter(ativo=True)
        data = []
        
        for estrutura in estruturas:
            estrutura_data = {
                'id': estrutura.id,
                'nome': estrutura.nome,
                'tipo': estrutura.tipo,
                'tipo_display': estrutura.get_tipo_display(),
                'descricao': estrutura.descricao,
                'custo_base': float(estrutura.custo_base),
                'custo_manutencao': float(estrutura.custo_manutencao),
                'custo_total_primeiro_ano': float(estrutura.get_custo_total_primeiro_ano()),
                'tempo_implementacao': estrutura.tempo_implementacao,
                'complexidade': estrutura.complexidade,
                'complexidade_display': estrutura.get_complexity_display_text(),
                
                # Tax information
                'impacto_tributario_eua': estrutura.impacto_tributario_eua,
                'impacto_tributario_brasil': estrutura.impacto_tributario_brasil,
                'impacto_tributario_outros': estrutura.impacto_tributario_outros,
                'formularios_obrigatorios_eua': estrutura.formularios_obrigatorios_eua,
                'formularios_obrigatorios_brasil': estrutura.formularios_obrigatorios_brasil,
                
                # Privacy and protection
                'nivel_confidencialidade': estrutura.nivel_confidencialidade,
                'protecao_patrimonial': estrutura.protecao_patrimonial,
                'impacto_privacidade': estrutura.impacto_privacidade,
                
                # Operational
                'facilidade_banking': estrutura.facilidade_banking,
                'documentacao_necessaria': estrutura.documentacao_necessaria,
            }
            data.append(estrutura_data)
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        logger.error(f"Error in estruturas_json: {str(e)}")
        return JsonResponse({'error': 'Failed to load structures'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def validar_configuracao(request):
    """
    Validates a configuration in real-time.
    Checks compatibility rules and returns errors, warnings, and suggestions.
    """
    try:
        data = json.loads(request.body)
        configuracao = data.get('configuracao', {})
        elementos = configuracao.get('elementos', [])
        
        if not elementos:
            return JsonResponse({
                'valido': True,
                'erros': [],
                'alertas': [],
                'sugestoes': []
            })
        
        estruturas_ids = [elemento.get('estrutura_id') for elemento in elementos if elemento.get('estrutura_id')]
        
        erros = []
        alertas = []
        sugestoes = []
        
        # Check validation rules between structures
        for i, id_a in enumerate(estruturas_ids):
            for id_b in estruturas_ids[i+1:]:
                # Check rules in both directions
                regras = RegraValidacao.objects.filter(
                    Q(estrutura_a_id=id_a, estrutura_b_id=id_b) |
                    Q(estrutura_a_id=id_b, estrutura_b_id=id_a),
                    ativo=True
                )
                
                for regra in regras:
                    if regra.tipo_relacionamento == 'INCOMPATIBLE':
                        if regra.severidade == 'ERROR':
                            erros.append({
                                'tipo': 'erro',
                                'severidade': 'ERROR',
                                'mensagem': regra.descricao,
                                'estruturas': [regra.estrutura_a.nome, regra.estrutura_b.nome]
                            })
                        else:
                            alertas.append({
                                'tipo': 'alerta',
                                'severidade': regra.severidade,
                                'mensagem': regra.descricao,
                                'estruturas': [regra.estrutura_a.nome, regra.estrutura_b.nome]
                            })
                    
                    elif regra.tipo_relacionamento == 'RECOMMENDED':
                        sugestoes.append({
                            'tipo': 'sugestao',
                            'severidade': 'INFO',
                            'mensagem': regra.descricao,
                            'estruturas': [regra.estrutura_a.nome, regra.estrutura_b.nome]
                        })
                    
                    elif regra.tipo_relacionamento == 'CONDITIONAL':
                        # Check if conditions are met
                        condicoes = regra.condicoes or {}
                        if not _verificar_condicoes(condicoes, elementos):
                            alertas.append({
                                'tipo': 'condicional',
                                'severidade': regra.severidade,
                                'mensagem': f"Conditional requirement: {regra.descricao}",
                                'estruturas': [regra.estrutura_a.nome, regra.estrutura_b.nome]
                            })
        
        # Check for missing required combinations
        estruturas_presentes = Estrutura.objects.filter(id__in=estruturas_ids)
        for estrutura in estruturas_presentes:
            regras_required = RegraValidacao.objects.filter(
                estrutura_a=estrutura,
                tipo_relacionamento='REQUIRED',
                ativo=True
            )
            
            for regra in regras_required:
                if regra.estrutura_b.id not in estruturas_ids:
                    if regra.severidade == 'ERROR':
                        erros.append({
                            'tipo': 'faltante',
                            'severidade': 'ERROR',
                            'mensagem': f"Required structure missing: {regra.descricao}",
                            'estrutura_faltante': regra.estrutura_b.nome
                        })
                    else:
                        sugestoes.append({
                            'tipo': 'recomendacao',
                            'severidade': 'INFO',
                            'mensagem': f"Consider adding: {regra.estrutura_b.nome} - {regra.descricao}",
                            'estrutura_sugerida': regra.estrutura_b.nome
                        })
        
        # Add jurisdiction-specific alerts
        alertas_jurisdicao = _get_alertas_jurisdicao(estruturas_presentes)
        alertas.extend(alertas_jurisdicao)
        
        return JsonResponse({
            'valido': len(erros) == 0,
            'erros': erros,
            'alertas': alertas,
            'sugestoes': sugestoes,
            'total_estruturas': len(estruturas_ids)
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error in validar_configuracao: {str(e)}")
        return JsonResponse({'error': 'Validation failed'}, status=500)


def _verificar_condicoes(condicoes, elementos):
    """
    Helper function to verify conditional requirements.
    """
    # Implement specific condition checking logic here
    # This is a placeholder for more complex conditional logic
    return True


def _get_alertas_jurisdicao(estruturas):
    """
    Get jurisdiction-specific alerts for the given structures.
    """
    alertas = []
    
    # Get alerts that apply to any of the structures
    alertas_aplicaveis = AlertaJurisdicao.objects.filter(
        ativo=True,
        estruturas_aplicaveis__in=estruturas
    ).distinct()
    
    for alerta in alertas_aplicaveis:
        alertas.append({
            'tipo': 'jurisdicao',
            'severidade': 'WARNING' if alerta.prioridade >= 4 else 'INFO',
            'mensagem': f"{alerta.get_jurisdicao_display()}: {alerta.titulo}",
            'descricao': alerta.descricao,
            'jurisdicao': alerta.jurisdicao
        })
    
    return alertas


@csrf_exempt
@require_http_methods(["POST"])
def salvar_template(request):
    """
    Saves a new template with complete configuration information.
    """
    try:
        data = json.loads(request.body)
        
        nome = data.get('nome')
        if not nome:
            return JsonResponse({'error': 'Template name is required'}, status=400)
        
        categoria = data.get('categoria', 'GENERAL')
        descricao = data.get('descricao', '')
        configuracao = data.get('configuracao', {})
        publico_alvo = data.get('publico_alvo', '')
        casos_uso = data.get('casos_uso', '')
        complexidade_template = data.get('complexidade_template', 'BASIC')
        
        # Calculate total cost and time
        elementos = configuracao.get('elementos', [])
        custo_total = 0
        tempo_total = 0
        
        for elemento in elementos:
            estrutura_id = elemento.get('estrutura_id')
            if estrutura_id:
                try:
                    estrutura = Estrutura.objects.get(id=estrutura_id)
                    custo_total += float(estrutura.custo_base)
                    tempo_total = max(tempo_total, estrutura.tempo_implementacao)
                except Estrutura.DoesNotExist:
                    continue
        
        template = Template.objects.create(
            nome=nome,
            categoria=categoria,
            complexidade_template=complexidade_template,
            descricao=descricao,
            configuracao=configuracao,
            custo_total=custo_total,
            tempo_total_implementacao=tempo_total,
            publico_alvo=publico_alvo,
            casos_uso=casos_uso
        )
        
        return JsonResponse({
            'status': 'success',
            'template_id': template.id,
            'message': 'Template saved successfully'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error in salvar_template: {str(e)}")
        return JsonResponse({'error': 'Failed to save template'}, status=500)


def carregar_template(request, template_id):
    """
    Loads a specific template configuration.
    """
    try:
        template = get_object_or_404(Template, id=template_id, ativo=True)
        template.incrementar_uso()
        
        return JsonResponse({
            'id': template.id,
            'nome': template.nome,
            'categoria': template.categoria,
            'descricao': template.descricao,
            'configuracao': template.configuracao,
            'custo_total': float(template.custo_total),
            'tempo_total': template.tempo_total_implementacao,
            'publico_alvo': template.publico_alvo,
            'casos_uso': template.casos_uso,
            'uso_count': template.uso_count
        })
    
    except Exception as e:
        logger.error(f"Error in carregar_template: {str(e)}")
        return JsonResponse({'error': 'Failed to load template'}, status=500)


def templates_json(request):
    """
    API endpoint returning available templates.
    """
    try:
        categoria = request.GET.get('categoria')
        search = request.GET.get('search')
        
        templates = Template.objects.filter(ativo=True)
        
        if categoria and categoria != 'ALL':
            templates = templates.filter(categoria=categoria)
        
        if search:
            templates = templates.filter(
                Q(nome__icontains=search) |
                Q(descricao__icontains=search) |
                Q(publico_alvo__icontains=search)
            )
        
        templates = templates.order_by('-uso_count', 'nome')
        
        data = []
        for template in templates:
            data.append({
                'id': template.id,
                'nome': template.nome,
                'categoria': template.categoria,
                'categoria_display': template.get_categoria_display(),
                'complexidade_template': template.complexidade_template,
                'descricao': template.descricao,
                'custo_total': float(template.custo_total),
                'tempo_total_implementacao': template.tempo_total_implementacao,
                'uso_count': template.uso_count,
                'publico_alvo': template.publico_alvo,
                'casos_uso': template.casos_uso
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        logger.error(f"Error in templates_json: {str(e)}")
        return JsonResponse({'error': 'Failed to load templates'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def salvar_configuracao(request):
    """
    Saves a user configuration (not a template).
    """
    try:
        data = json.loads(request.body)
        
        nome = data.get('nome')
        if not nome:
            return JsonResponse({'error': 'Configuration name is required'}, status=400)
        
        descricao = data.get('descricao', '')
        configuracao = data.get('configuracao', {})
        
        # Calculate estimates
        elementos = configuracao.get('elementos', [])
        custo_estimado = 0
        tempo_estimado = 0
        
        for elemento in elementos:
            estrutura_id = elemento.get('estrutura_id')
            if estrutura_id:
                try:
                    estrutura = Estrutura.objects.get(id=estrutura_id)
                    custo_estimado += float(estrutura.custo_base)
                    tempo_estimado = max(tempo_estimado, estrutura.tempo_implementacao)
                except Estrutura.DoesNotExist:
                    continue
        
        config_salva = ConfiguracaoSalva.objects.create(
            nome=nome,
            descricao=descricao,
            configuracao=configuracao,
            custo_estimado=custo_estimado,
            tempo_estimado=tempo_estimado
        )
        
        return JsonResponse({
            'status': 'success',
            'config_id': config_salva.id,
            'message': 'Configuration saved successfully'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error in salvar_configuracao: {str(e)}")
        return JsonResponse({'error': 'Failed to save configuration'}, status=500)


def admin_estruturas(request):
    """
    Simple admin interface for editing structures.
    """
    search = request.GET.get('search', '')
    tipo_filter = request.GET.get('tipo', '')
    
    estruturas = Estrutura.objects.all()
    
    if search:
        estruturas = estruturas.filter(
            Q(nome__icontains=search) |
            Q(descricao__icontains=search)
        )
    
    if tipo_filter:
        estruturas = estruturas.filter(tipo=tipo_filter)
    
    estruturas = estruturas.order_by('nome')
    
    # Pagination
    paginator = Paginator(estruturas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available types for filter
    tipos_disponiveis = Estrutura.TIPOS_ESTRUTURA
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'tipo_filter': tipo_filter,
        'tipos_disponiveis': tipos_disponiveis,
        'page_title': 'Structure Administration'
    }
    
    return render(request, 'admin_estruturas.html', context)


def estrutura_detail(request, estrutura_id):
    """
    Detailed view of a specific structure.
    """
    estrutura = get_object_or_404(Estrutura, id=estrutura_id)
    
    # Get related validation rules
    regras_como_a = RegraValidacao.objects.filter(estrutura_a=estrutura, ativo=True)
    regras_como_b = RegraValidacao.objects.filter(estrutura_b=estrutura, ativo=True)
    
    # Get applicable alerts
    alertas = AlertaJurisdicao.objects.filter(
        estruturas_aplicaveis=estrutura,
        ativo=True
    ).order_by('-prioridade')
    
    context = {
        'estrutura': estrutura,
        'regras_como_a': regras_como_a,
        'regras_como_b': regras_como_b,
        'alertas': alertas,
        'page_title': f'Structure Details: {estrutura.nome}'
    }
    
    return render(request, 'estrutura_detail.html', context)

