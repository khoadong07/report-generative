#!/usr/bin/env python3
"""
Template Renderer for HTML Reports
Renders HTML template with JSON data using simple string replacement
"""

import json
import re
from typing import Dict, Any


class TemplateRenderer:
    """Simple template renderer for HTML reports"""
    
    def __init__(self, template_path: str):
        """Initialize with template file path"""
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
    
    def render(self, data: Dict[str, Any]) -> str:
        """
        Render template with data
        
        Args:
            data: Dictionary containing template data
            
        Returns:
            Rendered HTML string
        """
        html = self.template
        
        # Replace JSON data placeholder
        html = html.replace('{{{json_data}}}', json.dumps(data, ensure_ascii=False, indent=2))
        
        # Replace simple variables like {{variable}}
        html = self._replace_simple_variables(html, data)
        
        # Replace nested variables like {{object.property}}
        html = self._replace_nested_variables(html, data)
        
        # Handle each loops for KPI cards
        html = self._handle_each_loops(html, data)
        
        return html
    
    def _replace_simple_variables(self, html: str, data: Dict[str, Any]) -> str:
        """Replace simple variables like {{variable}}"""
        pattern = r'\{\{([^{}#/]+)\}\}'
        
        def replace_var(match):
            var_name = match.group(1).strip()
            if var_name in data:
                return str(data[var_name])
            return match.group(0)  # Return original if not found
        
        return re.sub(pattern, replace_var, html)
    
    def _replace_nested_variables(self, html: str, data: Dict[str, Any]) -> str:
        """Replace nested variables like {{object.property}}"""
        pattern = r'\{\{([^{}#/]+\.[^{}#/]+)\}\}'
        
        def replace_nested_var(match):
            var_path = match.group(1).strip()
            try:
                value = self._get_nested_value(data, var_path)
                return str(value) if value is not None else ''
            except (KeyError, TypeError):
                return match.group(0)  # Return original if not found
        
        return re.sub(pattern, replace_nested_var, html)
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value from data using dot notation"""
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def _handle_each_loops(self, html: str, data: Dict[str, Any]) -> str:
        """Handle {{#each}} loops for arrays"""
        pattern = r'\{\{#each\s+([^}]+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_each(match):
            array_path = match.group(1).strip()
            template_content = match.group(2)
            
            try:
                # Get array data using nested path
                array_data = self._get_nested_value(data, array_path)
                
                if not isinstance(array_data, list):
                    print(f"Warning: {array_path} is not a list, got {type(array_data)}")
                    return ''
                
                result = ''
                for item in array_data:
                    item_html = template_content
                    
                    # Replace {{this.property}} with item values
                    this_pattern = r'\{\{this\.([^}]+)\}\}'
                    def replace_this(this_match):
                        prop = this_match.group(1).strip()
                        if isinstance(item, dict) and prop in item:
                            value = item[prop]
                            # Handle boolean values
                            if isinstance(value, bool):
                                return str(value).lower()
                            return str(value)
                        return ''
                    
                    item_html = re.sub(this_pattern, replace_this, item_html)
                    
                    # Handle conditional {{#if this.property}}...{{else}}...{{/if}}
                    if_pattern = r'\{\{#if\s+this\.([^}]+)\}\}(.*?)\{\{else\}\}(.*?)\{\{/if\}\}'
                    def replace_if(if_match):
                        prop = if_match.group(1).strip()
                        true_content = if_match.group(2)
                        false_content = if_match.group(3)
                        
                        if isinstance(item, dict) and prop in item:
                            value = item[prop]
                            # Check if value is truthy
                            if value:
                                return true_content
                            else:
                                return false_content
                        else:
                            return false_content
                    
                    item_html = re.sub(if_pattern, replace_if, item_html, flags=re.DOTALL)
                    
                    result += item_html
                
                return result
                
            except (KeyError, TypeError) as e:
                print(f"Warning: Error processing {array_path}: {e}")
                return ''
        
        return re.sub(pattern, replace_each, html, flags=re.DOTALL)
    
    def render_to_file(self, data: Dict[str, Any], output_path: str):
        """Render template and save to file"""
        rendered_html = self.render(data)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"Report rendered successfully to: {output_path}")


def main():
    """Main function to demonstrate usage"""
    # Load sample data
    with open('test/sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Render template
    renderer = TemplateRenderer('test/template_parameterized.html')
    renderer.render_to_file(data, 'test/rendered_report.html')
    
    print("Template rendered successfully!")
    print("Open 'test/rendered_report.html' in your browser to view the report.")


if __name__ == '__main__':
    main()