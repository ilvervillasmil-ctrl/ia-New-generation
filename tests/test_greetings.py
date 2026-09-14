"""
Tests for the Greetings Module
"""

import pytest
from core.greetings import GreetingSystem


def test_greeting_english():
    """Test basic English greeting"""
    gs = GreetingSystem()
    assert gs.greet('en') == 'Hello'


def test_greeting_spanish():
    """Test Spanish greeting (Hola)"""
    gs = GreetingSystem()
    assert gs.greet('es') == 'Hola'


def test_greeting_default():
    """Test default greeting is English"""
    gs = GreetingSystem()
    assert gs.greet() == 'Hello'


def test_greeting_unknown_language():
    """Test unknown language defaults to English"""
    gs = GreetingSystem()
    assert gs.greet('unknown') == 'Hello'


def test_greet_world_english():
    """Test 'Hello World' in English"""
    gs = GreetingSystem()
    assert gs.greet_world('en') == 'Hello World'


def test_greet_world_spanish():
    """Test 'Hola Mundo' in Spanish"""
    gs = GreetingSystem()
    assert gs.greet_world('es') == 'Hola Mundo'


def test_greet_world_french():
    """Test 'Bonjour Monde' in French"""
    gs = GreetingSystem()
    assert gs.greet_world('fr') == 'Bonjour Monde'


def test_greet_world_german():
    """Test 'Hallo Welt' in German"""
    gs = GreetingSystem()
    assert gs.greet_world('de') == 'Hallo Welt'


def test_all_greetings():
    """Test getting all greetings"""
    gs = GreetingSystem()
    all_greetings = gs.get_all_greetings()
    assert len(all_greetings) == 6
    assert any('Hola' in g for g in all_greetings)
    assert any('Hello' in g for g in all_greetings)


def test_welcome_message():
    """Test welcome message contains key framework elements"""
    gs = GreetingSystem()
    message = gs.welcome_message()
    assert 'Universal Integration System' in message
    assert 'Villasmil-Ω' in message
    assert 'α + β = 1' in message


def test_multiple_languages():
    """Test multiple language support"""
    gs = GreetingSystem()
    assert gs.greet('fr') == 'Bonjour'
    assert gs.greet('de') == 'Hallo'
    assert gs.greet('it') == 'Ciao'
    assert gs.greet('pt') == 'Olá'
