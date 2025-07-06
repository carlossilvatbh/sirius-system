from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Estrutura, RegraValidacao, AlertaJurisdicao, Product, PersonalizedProduct
from .cost_calculator import calculate_configuration_cost_django
from .validation_engine import validate_configuration_django
from .pdf_generator import generate_pdf_report

def test_canvas(request):
    """Test canvas for debugging."""
    return render(request, 'test_canvas.html')

def canvas_principal(request):
    """Main canvas interface for building legal structures."""
    context = {
        'page_title': 'SIRIUS Canvas - Legal Structure Designer'
    }
    return render(request, 'canvas_clean.html', context)

def canvas_modern(request):
    """Modern canvas interface with enhanced UX/UI."""
    context = {
        'page_title': 'SIRIUS Canvas v2.0 - Modern Interface'
    }
    return render(request, 'canvas_modern.html', context)

def admin_estruturas(request):
    """Admin interface for managing structures."""
    estruturas = Estrutura.objects.all()
    
    # Handle search
    search = request.GET.get('search', '')
    if search:
        estruturas = estruturas.filter(nome__icontains=search)
    
    # Handle type filter
    tipo = request.GET.get('tipo', '')
    if tipo:
        estruturas = estruturas.filter(tipo=tipo)
    
    context = {
        'estruturas': estruturas,
        'page_title': 'Structure Administration',
        'search': search,
        'tipo': tipo
    }
    return render(request, 'admin_estruturas.html', context)

def estrutura_detail(request, estrutura_id):
    """View for structure details."""
    estrutura = get_object_or_404(Estrutura, id=estrutura_id)
    context = {
        'estrutura': estrutura,
        'page_title': f'Structure Details - {estrutura.nome}'
    }
    return render(request, 'estrutura_detail.html', context)


# API Endpoints

@require_http_methods(["GET"])
def api_estruturas(request):
    """API endpoint to get all available structures."""
    try:
        estruturas = Estrutura.objects.all()
        data = []
        
        for estrutura in estruturas:
            data.append({
                'id': estrutura.id,
                'tipo': estrutura.tipo,
                'nome': estrutura.nome,
                'descricao': estrutura.descricao,
                'custo_base': float(estrutura.custo_base),
                'custo_manutencao': float(estrutura.custo_manutencao),
                'tempo_implementacao': estrutura.tempo_implementacao,
                'complexidade': estrutura.complexidade,
                'nivel_confidencialidade': estrutura.nivel_confidencialidade,
                'impacto_tributario_eua': estrutura.impacto_tributario_eua,
                'impacto_tributario_brasil': estrutura.impacto_tributario_brasil,
                'impacto_tributario_outros': estrutura.impacto_tributario_outros,
                'protecao_patrimonial': estrutura.protecao_patrimonial,
                'impacto_privacidade': estrutura.impacto_privacidade,
                'facilidade_banking': estrutura.facilidade_banking,
                'documentacao_necessaria': estrutura.documentacao_necessaria.split('\n') if estrutura.documentacao_necessaria else [],
                'formularios_obrigatorios_eua': estrutura.formularios_obrigatorios_eua,
                'formularios_obrigatorios_brasil': estrutura.formularios_obrigatorios_brasil,
                'ativo': estrutura.ativo
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_templates(request):
    """API endpoint to get all available templates."""
    try:
        templates = Product.objects.filter(ativo=True)
        data = []
        
        for template in templates:
            # Handle configuracao field (already a dict if JSONField)
            configuracao = template.configuracao if template.configuracao else {}
            
            data.append({
                'id': template.id,
                'nome': template.nome,
                'categoria': template.categoria,
                'complexidade_template': template.complexidade_template,
                'descricao': template.descricao,
                'configuracao': configuracao,
                'custo_total': float(template.custo_total),
                'tempo_total_implementacao': template.tempo_total_implementacao,
                'uso_count': template.uso_count,
                'publico_alvo': template.publico_alvo
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_calcular_custos(request):
    """API endpoint for advanced cost calculation."""
    try:
        data = json.loads(request.body)
        elementos = data.get('elementos', [])
        cenario = data.get('cenario', 'basic')
        incluir_analise_risco = data.get('incluir_analise_risco', True)
        
        if not elementos:
            return JsonResponse({'error': 'No structures provided'}, status=400)
        
        # Convert elementos to structure data format
        estruturas_data = []
        for elemento in elementos:
            estrutura_id = elemento.get('estrutura', {}).get('id')
            if estrutura_id:
                try:
                    estrutura = Estrutura.objects.get(id=estrutura_id)
                    estruturas_data.append({
                        'id': estrutura.id,
                        'tipo': estrutura.tipo,
                        'custo_base': float(estrutura.custo_base),
                        'custo_manutencao': float(estrutura.custo_manutencao),
                        'complexidade': estrutura.complexidade,
                        'tempo_implementacao': estrutura.tempo_implementacao,
                        'nivel_confidencialidade': estrutura.nivel_confidencialidade
                    })
                except Estrutura.DoesNotExist:
                    continue
        
        # Calculate costs using advanced calculator
        resultado = calculate_configuration_cost_django(
            estruturas_data, 
            cenario, 
            incluir_analise_risco
        )
        
        return JsonResponse(resultado)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_validar_configuracao(request):
    """API endpoint for advanced configuration validation."""
    try:
        data = json.loads(request.body)
        elementos = data.get('elementos', [])
        analise_custos = data.get('analise_custos')
        
        if not elementos:
            return JsonResponse({'error': 'No structures provided'}, status=400)
        
        # Convert elementos to structure data format
        estruturas_data = []
        for elemento in elementos:
            estrutura_id = elemento.get('estrutura_id')
            if estrutura_id:
                try:
                    estrutura = Estrutura.objects.get(id=estrutura_id)
                    estruturas_data.append({
                        'id': estrutura.id,
                        'tipo': estrutura.tipo,
                        'custo_base': float(estrutura.custo_base),
                        'custo_manutencao': float(estrutura.custo_manutencao),
                        'complexidade': estrutura.complexidade,
                        'tempo_implementacao': estrutura.tempo_implementacao,
                        'nivel_confidencialidade': estrutura.nivel_confidencialidade
                    })
                except Estrutura.DoesNotExist:
                    continue
        
        # If no valid structures found, return a basic validation result
        if not estruturas_data:
            return JsonResponse({
                'is_valid': True,
                'total_issues': 0,
                'critical_count': 0,
                'error_count': 0,
                'warning_count': 0,
                'info_count': 0,
                'overall_score': 100.0,
                'recommendations': [],
                'results': []
            })
        
        # Validate configuration using advanced validator
        resultado = validate_configuration_django(estruturas_data, analise_custos)
        
        return JsonResponse(resultado)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_regras_validacao(request):
    """API endpoint to get validation rules."""
    try:
        regras = RegraValidacao.objects.filter(ativa=True)
        data = []
        
        for regra in regras:
            data.append({
                'id': regra.id,
                'estrutura_origem': regra.estrutura_origem.tipo if regra.estrutura_origem else None,
                'estrutura_destino': regra.estrutura_destino.tipo if regra.estrutura_destino else None,
                'tipo_regra': regra.tipo_regra,
                'nivel_severidade': regra.nivel_severidade,
                'mensagem': regra.mensagem,
                'descricao': regra.descricao,
                'recomendacao': regra.recomendacao
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_alertas_jurisdicao(request):
    """API endpoint to get jurisdiction alerts."""
    try:
        alertas = AlertaJurisdicao.objects.filter(ativo=True)
        data = []
        
        for alerta in alertas:
            data.append({
                'id': alerta.id,
                'jurisdicao': alerta.jurisdicao,
                'tipo_alerta': alerta.tipo_alerta,
                'titulo': alerta.titulo,
                'mensagem': alerta.mensagem,
                'nivel_prioridade': alerta.nivel_prioridade,
                'data_inicio': alerta.data_inicio.isoformat() if alerta.data_inicio else None,
                'data_fim': alerta.data_fim.isoformat() if alerta.data_fim else None
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        # Return empty list instead of error for missing data
        return JsonResponse([], safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def api_salvar_configuracao(request):
    """API endpoint to save a configuration."""
    try:
        data = json.loads(request.body)
        nome = data.get('nome')
        descricao = data.get('descricao', '')
        elementos = data.get('elementos', [])
        
        if not nome or not elementos:
            return JsonResponse({'error': 'Name and elements are required'}, status=400)
        
        # Create configuration
        configuracao = PersonalizedProduct.objects.create(
            nome=nome,
            descricao=descricao,
            configuracao_json=json.dumps(elementos),
            custo_total=data.get('custo_total', 0),
            tempo_total=data.get('tempo_total', 0)
        )
        
        return JsonResponse({
            'id': configuracao.id,
            'message': 'Configuration saved successfully'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_configuracoes_salvas(request):
    """API endpoint to get saved configurations."""
    try:
        configuracoes = PersonalizedProduct.objects.all().order_by('-created_at')
        data = []
        
        for config in configuracoes:
            try:
                elementos = json.loads(config.configuracao_json) if config.configuracao_json else []
            except json.JSONDecodeError:
                elementos = []
            
            data.append({
                'id': config.id,
                'nome': config.nome,
                'descricao': config.descricao,
                'elementos': elementos,
                'custo_total': float(config.custo_total),
                'tempo_total': config.tempo_total,
                'data_criacao': config.data_criacao.isoformat(),
                'data_modificacao': config.data_modificacao.isoformat()
            })
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_aplicar_template(request):
    """API endpoint to apply a template."""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        
        if not template_id:
            return JsonResponse({'error': 'Template ID is required'}, status=400)
        
        try:
            template = Product.objects.get(id=template_id, ativo=True)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Template not found'}, status=404)
        
        # Parse estruturas_ids
        try:
            estruturas_ids = json.loads(template.estruturas_ids) if template.estruturas_ids else []
        except json.JSONDecodeError:
            estruturas_ids = []
        
        # Get structures
        estruturas = Estrutura.objects.filter(id__in=estruturas_ids, ativo=True)
        elementos = []
        
        for i, estrutura in enumerate(estruturas):
            elementos.append({
                'id': f'template_{template_id}_{estrutura.id}_{i}',
                'estrutura': {
                    'id': estrutura.id,
                    'tipo': estrutura.tipo,
                    'nome': estrutura.nome,
                    'descricao': estrutura.descricao,
                    'custo_base': float(estrutura.custo_base),
                    'custo_manutencao': float(estrutura.custo_manutencao),
                    'tempo_implementacao': estrutura.tempo_implementacao,
                    'complexidade': estrutura.complexidade,
                    'nivel_confidencialidade': estrutura.nivel_confidencialidade,
                    'implicacoes_fiscais': estrutura.implicacoes_fiscais,
                    'vantagens': estrutura.vantagens.split('\n') if estrutura.vantagens else [],
                    'desvantagens': estrutura.desvantagens.split('\n') if estrutura.desvantagens else [],
                    'documentos_necessarios': estrutura.documentos_necessarios.split('\n') if estrutura.documentos_necessarios else []
                },
                'position': {
                    'x': 100 + (i % 3) * 250,  # Arrange in grid
                    'y': 100 + (i // 3) * 150
                }
            })
        
        # Increment template usage
        template.usos += 1
        template.save()
        
        return JsonResponse({
            'elementos': elementos,
            'template': {
                'id': template.id,
                'nome': template.nome,
                'descricao': template.descricao,
                'setor': template.setor
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def api_generate_pdf(request):
    """Generate PDF report for a configuration."""
    try:
        data = json.loads(request.body)
        
        # Get configuration data
        configuration_data = data.get('configuration', {})
        canvas_image_base64 = data.get('canvas_image', None)
        
        # Validate configuration data
        if not configuration_data:
            return JsonResponse({'error': 'Configuration data is required'}, status=400)
        
        # Enrich configuration data with structure details
        elementos = configuration_data.get('elementos', [])
        enriched_elementos = []
        
        for elemento in elementos:
            estrutura_id = elemento.get('estrutura_id')
            if estrutura_id:
                try:
                    estrutura = Estrutura.objects.get(id=estrutura_id)
                    elemento_enriched = elemento.copy()
                    elemento_enriched['estrutura'] = {
                        'id': estrutura.id,
                        'nome': estrutura.nome,
                        'tipo': estrutura.tipo,
                        'descricao': estrutura.descricao,
                        'custo_base': float(estrutura.custo_base),
                        'custo_manutencao': float(estrutura.custo_manutencao),
                        'tempo_implementacao': estrutura.tempo_implementacao,
                        'complexidade': estrutura.complexidade,
                        'nivel_confidencialidade': estrutura.nivel_confidencialidade,
                        'impacto_tributario_eua': estrutura.impacto_tributario_eua,
                        'impacto_tributario_brasil': estrutura.impacto_tributario_brasil,
                        'impacto_tributario_outros': estrutura.impacto_tributario_outros,
                        'protecao_patrimonial': estrutura.protecao_patrimonial,
                        'impacto_privacidade': estrutura.impacto_privacidade,
                        'facilidade_banking': estrutura.facilidade_banking,
                        'documentacao_necessaria': estrutura.documentacao_necessaria,
                        'formularios_obrigatorios_eua': estrutura.formularios_obrigatorios_eua,
                        'formularios_obrigatorios_brasil': estrutura.formularios_obrigatorios_brasil
                    }
                    enriched_elementos.append(elemento_enriched)
                except Estrutura.DoesNotExist:
                    continue
        
        # Update configuration with enriched data
        enriched_configuration = configuration_data.copy()
        enriched_configuration['elementos'] = enriched_elementos
        
        # Calculate costs and analysis
        try:
            cost_result = calculate_configuration_cost_django(enriched_configuration)
            enriched_configuration.update(cost_result)
        except Exception as e:
            # If cost calculation fails, continue without it
            pass
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(enriched_configuration, canvas_image_base64)
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sirius_structure_report.pdf"'
        response['Content-Length'] = len(pdf_buffer.getvalue())
        
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'PDF generation failed: {str(e)}'}, status=500)

