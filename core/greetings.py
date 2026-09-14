"""
Greetings Module for Universal Integration System
Demonstrates basic functionality with multilingual support
"""

from typing import Dict, List


class GreetingSystem:
    """
    A simple greeting system that demonstrates the Universal Integration 
    System's multilingual capability and welcoming nature.
    """
    
    def __init__(self):
        """Initialize the greeting system with supported languages."""
        self.greetings: Dict[str, str] = {
            'en': 'Hello',
            'es': 'Hola',
            'fr': 'Bonjour',
            'de': 'Hallo',
            'it': 'Ciao',
            'pt': 'Olá'
        }
        self.world_translations: Dict[str, str] = {
            'en': 'World',
            'es': 'Mundo',
            'fr': 'Monde',
            'de': 'Welt',
            'it': 'Mondo',
            'pt': 'Mundo'
        }
    
    def greet(self, language: str = 'en') -> str:
        """
        Return a greeting in the specified language.
        
        Args:
            language: Language code (default: 'en')
        
        Returns:
            Greeting string in the specified language
        """
        return self.greetings.get(language.lower(), self.greetings['en'])
    
    def greet_world(self, language: str = 'en') -> str:
        """
        Return a 'Hello World' greeting in the specified language.
        
        Args:
            language: Language code (default: 'en')
        
        Returns:
            'Hello World' string in the specified language
        """
        greeting = self.greet(language)
        world = self.world_translations.get(language.lower(), self.world_translations['en'])
        return f"{greeting} {world}"
    
    def get_all_greetings(self) -> List[str]:
        """
        Get greetings in all supported languages.
        
        Returns:
            List of all greetings
        """
        return [f"{self.greet(lang)} ({lang.upper()})" 
                for lang in self.greetings.keys()]
    
    def welcome_message(self) -> str:
        """
        Return the Universal Integration System welcome message.
        
        Returns:
            Welcome message string
        """
        return (
            "Welcome to the Universal Integration System\n"
            "Villasmil-Ω Framework\n"
            "Where Order and Mystery unite: α + β = 1"
        )
