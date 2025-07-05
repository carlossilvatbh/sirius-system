"""
SIRIUS PDF Generation System
Generates professional PDF reports for legal structure configurations.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from io import BytesIO
import base64
from datetime import datetime
import json
from decimal import Decimal
from django.conf import settings
import os


class SiriusPDFGenerator:
    """
    Professional PDF generator for SIRIUS legal structure reports.
    Creates comprehensive reports with structure analysis, cost breakdown, and recommendations.
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF."""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1e40af'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#374151'),
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=HexColor('#1f2937'),
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            textColor=HexColor('#374151'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=HexColor('#059669'),
            fontName='Helvetica-Bold'
        ))
        
        # Warning style
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            textColor=HexColor('#dc2626'),
            fontName='Helvetica-Bold'
        ))

    def generate_structure_report(self, configuration_data, canvas_image_base64=None):
        """
        Generate a comprehensive PDF report for a legal structure configuration.
        
        Args:
            configuration_data (dict): Complete configuration data including structures, costs, etc.
            canvas_image_base64 (str): Base64 encoded image of the canvas (optional)
            
        Returns:
            BytesIO: PDF file as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the story (content)
        story = []
        
        # Title page
        story.extend(self._build_title_page(configuration_data))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._build_executive_summary(configuration_data))
        story.append(PageBreak())
        
        # Structure overview
        story.extend(self._build_structure_overview(configuration_data))
        
        # Canvas visualization (if provided)
        if canvas_image_base64:
            story.append(PageBreak())
            story.extend(self._build_canvas_visualization(canvas_image_base64))
        
        # Cost analysis
        story.append(PageBreak())
        story.extend(self._build_cost_analysis(configuration_data))
        
        # Tax implications
        story.append(PageBreak())
        story.extend(self._build_tax_implications(configuration_data))
        
        # Implementation timeline
        story.append(PageBreak())
        story.extend(self._build_implementation_timeline(configuration_data))
        
        # Recommendations
        story.append(PageBreak())
        story.extend(self._build_recommendations(configuration_data))
        
        # Appendices
        story.append(PageBreak())
        story.extend(self._build_appendices(configuration_data))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _build_title_page(self, config):
        """Build the title page of the report."""
        story = []
        
        # Main title
        story.append(Paragraph("SIRIUS", self.styles['CustomTitle']))
        story.append(Paragraph("Strategic Intelligence Relationship & Interactive Universal System", 
                              self.styles['CustomSubtitle']))
        story.append(Spacer(1, 50))
        
        # Report title
        story.append(Paragraph("Legal Structure Configuration Report", 
                              self.styles['CustomSubtitle']))
        story.append(Spacer(1, 30))
        
        # Configuration details
        config_name = config.get('name', 'Custom Configuration')
        story.append(Paragraph(f"Configuration: <b>{config_name}</b>", 
                              self.styles['CustomBody']))
        
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Generated: {current_date}", 
                              self.styles['CustomBody']))
        story.append(Spacer(1, 50))
        
        # Summary table
        summary_data = [
            ['Total Structures', str(len(config.get('elementos', [])))],
            ['Total Cost', f"${config.get('custo_total', 0):,.2f}"],
            ['Implementation Time', f"{config.get('tempo_total', 0)} days"],
            ['Scenario', config.get('cenario', 'Basic').title()]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb'))
        ]))
        
        story.append(summary_table)
        
        return story

    def _build_executive_summary(self, config):
        """Build the executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['CustomSubtitle']))
        
        # Overview
        elementos = config.get('elementos', [])
        total_cost = config.get('custo_total', 0)
        total_time = config.get('tempo_total', 0)
        
        summary_text = f"""
        This report presents a comprehensive analysis of your legal structure configuration 
        consisting of {len(elementos)} carefully selected entities. The proposed structure 
        has been designed to optimize tax efficiency, asset protection, and operational 
        flexibility while maintaining compliance across multiple jurisdictions.
        
        The total implementation cost is estimated at ${total_cost:,.2f} with a projected 
        timeline of {total_time} days. This configuration has been validated against 
        current regulatory requirements and best practices in international structuring.
        """
        
        story.append(Paragraph(summary_text, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Key benefits
        story.append(Paragraph("Key Benefits", self.styles['SectionHeader']))
        
        benefits = [
            "Optimized tax efficiency across multiple jurisdictions",
            "Enhanced asset protection and privacy",
            "Streamlined operational structure",
            "Regulatory compliance assurance",
            "Scalable framework for future growth"
        ]
        
        for benefit in benefits:
            story.append(Paragraph(f"• {benefit}", self.styles['CustomBody']))
        
        return story

    def _build_structure_overview(self, config):
        """Build the structure overview section."""
        story = []
        
        story.append(Paragraph("Structure Overview", self.styles['CustomSubtitle']))
        
        elementos = config.get('elementos', [])
        
        if not elementos:
            story.append(Paragraph("No structures configured.", self.styles['CustomBody']))
            return story
        
        # Structure table
        table_data = [['Structure', 'Type', 'Cost', 'Implementation Time', 'Complexity']]
        
        for elemento in elementos:
            estrutura = elemento.get('estrutura', {})
            table_data.append([
                estrutura.get('nome', 'Unknown'),
                estrutura.get('tipo', 'Unknown'),
                f"${estrutura.get('custo_base', 0):,.2f}",
                f"{estrutura.get('tempo_implementacao', 0)} days",
                f"Level {estrutura.get('complexidade', 1)}"
            ])
        
        structure_table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        structure_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9fafb')])
        ]))
        
        story.append(structure_table)
        story.append(Spacer(1, 20))
        
        # Detailed descriptions
        story.append(Paragraph("Detailed Structure Descriptions", self.styles['SectionHeader']))
        
        for i, elemento in enumerate(elementos, 1):
            estrutura = elemento.get('estrutura', {})
            story.append(Paragraph(f"{i}. {estrutura.get('nome', 'Unknown Structure')}", 
                                  self.styles['Highlight']))
            story.append(Paragraph(estrutura.get('descricao', 'No description available.'), 
                                  self.styles['CustomBody']))
            story.append(Spacer(1, 10))
        
        return story

    def _build_canvas_visualization(self, canvas_image_base64):
        """Build the canvas visualization section."""
        story = []
        
        story.append(Paragraph("Structure Visualization", self.styles['CustomSubtitle']))
        story.append(Paragraph("The following diagram shows the visual representation of your configured legal structure:", 
                              self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        try:
            # Decode base64 image
            image_data = base64.b64decode(canvas_image_base64.split(',')[1])
            image_buffer = BytesIO(image_data)
            
            # Add image to story
            img = Image(image_buffer, width=6*inch, height=4*inch)
            story.append(img)
            
        except Exception as e:
            story.append(Paragraph(f"Error loading canvas image: {str(e)}", 
                                  self.styles['Warning']))
        
        return story

    def _build_cost_analysis(self, config):
        """Build the cost analysis section."""
        story = []
        
        story.append(Paragraph("Cost Analysis", self.styles['CustomSubtitle']))
        
        # Cost breakdown
        analise = config.get('analise_detalhada', {})
        breakdown = analise.get('breakdown', {})
        
        if breakdown:
            cost_data = [['Category', 'Amount', 'Percentage']]
            total = analise.get('custo_total', 1)
            
            for category, amount in breakdown.items():
                percentage = (amount / total * 100) if total > 0 else 0
                cost_data.append([
                    category.replace('_', ' ').title(),
                    f"${amount:,.2f}",
                    f"{percentage:.1f}%"
                ])
            
            # Add total row
            cost_data.append(['TOTAL', f"${total:,.2f}", '100.0%'])
            
            cost_table = Table(cost_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
            cost_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-2, -1), white),
                ('BACKGROUND', (0, -1), (-1, -1), HexColor('#f3f4f6')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            story.append(cost_table)
        
        story.append(Spacer(1, 20))
        
        # Scenario comparison
        story.append(Paragraph("Scenario Comparison", self.styles['SectionHeader']))
        
        scenario_text = """
        The cost analysis includes three different scenarios to help you understand 
        the investment required at different service levels:
        
        • Basic Scenario: Essential setup costs only
        • Complete Scenario: Includes professional consultation and documentation
        • Premium Scenario: Full-service implementation with ongoing support
        """
        
        story.append(Paragraph(scenario_text, self.styles['CustomBody']))
        
        return story

    def _build_tax_implications(self, config):
        """Build the tax implications section."""
        story = []
        
        story.append(Paragraph("Tax Implications", self.styles['CustomSubtitle']))
        
        elementos = config.get('elementos', [])
        
        # US tax implications
        story.append(Paragraph("United States", self.styles['SectionHeader']))
        us_implications = []
        
        for elemento in elementos:
            estrutura = elemento.get('estrutura', {})
            us_impact = estrutura.get('impacto_tributario_eua', '')
            if us_impact:
                us_implications.append(f"• {estrutura.get('nome', 'Structure')}: {us_impact}")
        
        if us_implications:
            for implication in us_implications:
                story.append(Paragraph(implication, self.styles['CustomBody']))
        else:
            story.append(Paragraph("No specific US tax implications identified.", 
                                  self.styles['CustomBody']))
        
        story.append(Spacer(1, 15))
        
        # Brazil tax implications
        story.append(Paragraph("Brazil", self.styles['SectionHeader']))
        brazil_implications = []
        
        for elemento in elementos:
            estrutura = elemento.get('estrutura', {})
            brazil_impact = estrutura.get('impacto_tributario_brasil', '')
            if brazil_impact:
                brazil_implications.append(f"• {estrutura.get('nome', 'Structure')}: {brazil_impact}")
        
        if brazil_implications:
            for implication in brazil_implications:
                story.append(Paragraph(implication, self.styles['CustomBody']))
        else:
            story.append(Paragraph("No specific Brazil tax implications identified.", 
                                  self.styles['CustomBody']))
        
        return story

    def _build_implementation_timeline(self, config):
        """Build the implementation timeline section."""
        story = []
        
        story.append(Paragraph("Implementation Timeline", self.styles['CustomSubtitle']))
        
        elementos = config.get('elementos', [])
        
        if not elementos:
            story.append(Paragraph("No implementation timeline available.", 
                                  self.styles['CustomBody']))
            return story
        
        # Timeline table
        timeline_data = [['Phase', 'Structure', 'Duration', 'Key Activities']]
        
        for i, elemento in enumerate(elementos, 1):
            estrutura = elemento.get('estrutura', {})
            timeline_data.append([
                f"Phase {i}",
                estrutura.get('nome', 'Unknown'),
                f"{estrutura.get('tempo_implementacao', 0)} days",
                "Setup, documentation, registration"
            ])
        
        timeline_table = Table(timeline_data, colWidths=[1*inch, 2*inch, 1*inch, 2.5*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9fafb')])
        ]))
        
        story.append(timeline_table)
        
        return story

    def _build_recommendations(self, config):
        """Build the recommendations section."""
        story = []
        
        story.append(Paragraph("Recommendations", self.styles['CustomSubtitle']))
        
        recommendations = [
            "Engage qualified legal counsel in each relevant jurisdiction before implementation",
            "Consider phased implementation to manage cash flow and complexity",
            "Establish proper documentation and compliance procedures from the outset",
            "Regular review of structure effectiveness and regulatory changes",
            "Maintain detailed records for all inter-entity transactions"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        story.append(Spacer(1, 20))
        
        # Disclaimer
        story.append(Paragraph("Important Disclaimer", self.styles['SectionHeader']))
        disclaimer = """
        This report is for informational purposes only and does not constitute legal, 
        tax, or financial advice. The information contained herein is based on current 
        understanding of applicable laws and regulations, which are subject to change. 
        You should consult with qualified professionals before implementing any legal 
        structure or making any financial decisions.
        """
        
        story.append(Paragraph(disclaimer, self.styles['Warning']))
        
        return story

    def _build_appendices(self, config):
        """Build the appendices section."""
        story = []
        
        story.append(Paragraph("Appendices", self.styles['CustomSubtitle']))
        
        # Appendix A: Structure Details
        story.append(Paragraph("Appendix A: Detailed Structure Information", 
                              self.styles['SectionHeader']))
        
        elementos = config.get('elementos', [])
        
        for i, elemento in enumerate(elementos, 1):
            estrutura = elemento.get('estrutura', {})
            
            story.append(Paragraph(f"A.{i} {estrutura.get('nome', 'Unknown Structure')}", 
                                  self.styles['Highlight']))
            
            # Structure details table
            details_data = [
                ['Type', estrutura.get('tipo', 'Unknown')],
                ['Base Cost', f"${estrutura.get('custo_base', 0):,.2f}"],
                ['Maintenance Cost', f"${estrutura.get('custo_manutencao', 0):,.2f}"],
                ['Implementation Time', f"{estrutura.get('tempo_implementacao', 0)} days"],
                ['Complexity Level', f"Level {estrutura.get('complexidade', 1)}"],
                ['Confidentiality Level', f"Level {estrutura.get('nivel_confidencialidade', 1)}"],
                ['Asset Protection Level', f"Level {estrutura.get('protecao_patrimonial', 1)}"],
                ['Banking Facility', f"Level {estrutura.get('facilidade_banking', 1)}"]
            ]
            
            details_table = Table(details_data, colWidths=[2*inch, 3*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#f3f4f6')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            story.append(details_table)
            story.append(Spacer(1, 15))
        
        return story


def generate_pdf_report(configuration_data, canvas_image_base64=None):
    """
    Convenience function to generate a PDF report.
    
    Args:
        configuration_data (dict): Configuration data
        canvas_image_base64 (str): Base64 encoded canvas image
        
    Returns:
        BytesIO: PDF file buffer
    """
    generator = SiriusPDFGenerator()
    return generator.generate_structure_report(configuration_data, canvas_image_base64)

