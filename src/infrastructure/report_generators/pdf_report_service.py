"""
PDF report generation service implementation using ReportLab.
"""

import os
from typing import Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from ...domain.entities.sales_order import SalesOrder
from ...domain.services.report_generation_service import ReportGenerationService
from ...shared.exceptions.exceptions import ReportGenerationException
from ...shared.utils.config import config
from ...shared.utils.format_utils import FormatUtils


class PdfReportGenerationService(ReportGenerationService):
    """PDF report generation service implementation using ReportLab."""
    
    def __init__(self):
        """Initialize service with configuration."""
        self._supported_formats = ['PDF']
        config.ensure_directories_exist()
    
    def generate_sales_order_report(self, sales_order: SalesOrder, output_path: Optional[str] = None) -> str:
        """
        Generate sales order report in PDF format.
        
        Args:
            sales_order: The sales order to generate report for
            output_path: Optional custom output path
            
        Returns:
            Path to the generated report file
        """
        try:
            # Generate file path
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sales_order_{sales_order.id}_{timestamp}.pdf"
                output_path = config.get_full_reports_path(filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            styles = getSampleStyleSheet()
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("SALES ORDER RECEIPT", title_style))
            story.append(Spacer(1, 12))
            
            # Add order information
            order_info_style = ParagraphStyle(
                'OrderInfo',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=6
            )
            
            story.append(Paragraph(f"<b>Order ID:</b> {sales_order.id}", order_info_style))
            story.append(Paragraph(f"<b>Date:</b> {sales_order.created_at.strftime('%d/%m/%Y %H:%M')}", order_info_style))
            story.append(Spacer(1, 12))
            
            # Add customer information
            customer_title_style = ParagraphStyle(
                'CustomerTitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12
            )
            story.append(Paragraph("CUSTOMER INFORMATION", customer_title_style))
            
            customer_info_style = ParagraphStyle(
                'CustomerInfo',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=4
            )
            
            story.append(Paragraph(f"<b>Company:</b> {sales_order.company.name}", customer_info_style))
            story.append(Paragraph(f"<b>Document:</b> {sales_order.company.document.get_formatted()}", customer_info_style))
            story.append(Paragraph(f"<b>Email:</b> {sales_order.company.contact.email}", customer_info_style))
            story.append(Paragraph(f"<b>Phone:</b> {sales_order.company.contact.get_formatted_phone()}", customer_info_style))
            
            # Add address
            address_lines = sales_order.company.address.get_full_address().split('\n')
            for line in address_lines:
                if line.strip():
                    story.append(Paragraph(f"<b>Address:</b> {line.strip()}", customer_info_style))
                    break
            
            for line in address_lines[1:]:
                if line.strip():
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{line.strip()}", customer_info_style))
            
            story.append(Spacer(1, 20))
            
            # Add items table
            items_title_style = ParagraphStyle(
                'ItemsTitle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=12
            )
            story.append(Paragraph("ORDER ITEMS", items_title_style))
            
            # Create table data
            table_data = [
                ['SKU', 'Product', 'Qty', 'Unit Price', 'Subtotal']
            ]
            
            for item in sales_order.items:
                table_data.append([
                    item.product.sku,
                    item.product.name[:30] + '...' if len(item.product.name) > 30 else item.product.name,
                    str(item.quantity),
                    FormatUtils.format_currency(item.unit_price),
                    FormatUtils.format_currency(item.subtotal)
                ])
            
            # Create table
            table = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1.2*inch, 1.2*inch])
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Quantity column
                ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),  # Price columns
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
            
            # Add totals
            totals_style = ParagraphStyle(
                'Totals',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_RIGHT,
                spaceAfter=6
            )
            
            story.append(Paragraph(f"<b>Total Items: {sales_order.total_items}</b>", totals_style))
            story.append(Paragraph(f"<b>Total Amount: {FormatUtils.format_currency(sales_order.total_amount)}</b>", totals_style))
            story.append(Spacer(1, 30))
            
            # Add footer
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
            
            story.append(Paragraph("Thank you for your business!", footer_style))
            story.append(Paragraph(f"Report generated on {datetime.now().strftime('%d/%m/%Y at %H:%M')}", footer_style))
            
            # Build PDF
            doc.build(story)
            
            return output_path
            
        except Exception as e:
            raise ReportGenerationException(f"Failed to generate PDF report: {str(e)}", "PDF")
    
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported report formats.
        
        Returns:
            List of supported formats
        """
        return self._supported_formats.copy()
