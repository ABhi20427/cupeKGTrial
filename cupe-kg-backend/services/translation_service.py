"""
Translation Service for CuPe-KG
Provides translation functionality using Google Translate for multilingual support
"""

from deep_translator import GoogleTranslator
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Language code mapping
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi'
}

# Simple in-memory cache for translations
translation_cache = {}

def get_cache_key(text: str, source_lang: str, target_lang: str) -> str:
    """Generate a cache key for translation"""
    return f"{source_lang}:{target_lang}:{text[:100]}"

def translate_text(text: str, target_lang: str, source_lang: str = 'en') -> str:
    """
    Translate text from source language to target language

    Args:
        text: Text to translate
        target_lang: Target language code (e.g., 'hi', 'bn', 'ta')
        source_lang: Source language code (default: 'en')

    Returns:
        Translated text
    """
    if not text or not text.strip():
        return text

    # If source and target are the same, return original text
    if source_lang == target_lang:
        return text

    # Check if target language is supported
    if target_lang not in SUPPORTED_LANGUAGES:
        logger.warning(f"Unsupported target language: {target_lang}")
        return text

    # Check cache first
    cache_key = get_cache_key(text, source_lang, target_lang)
    if cache_key in translation_cache:
        logger.info(f"Cache hit for translation: {cache_key[:50]}...")
        return translation_cache[cache_key]

    try:
        # Perform translation
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)

        # Cache the result
        translation_cache[cache_key] = translated

        logger.info(f"Translated text from {source_lang} to {target_lang}")
        return translated

    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return text  # Return original text on error

def translate_dict(data: Dict, target_lang: str, source_lang: str = 'en',
                   fields_to_translate: Optional[List[str]] = None) -> Dict:
    """
    Translate specific fields in a dictionary

    Args:
        data: Dictionary containing text to translate
        target_lang: Target language code
        source_lang: Source language code (default: 'en')
        fields_to_translate: List of field names to translate (if None, translates common fields)

    Returns:
        Dictionary with translated fields
    """
    if target_lang == source_lang or target_lang == 'en':
        return data

    # Default fields to translate if not specified
    if fields_to_translate is None:
        fields_to_translate = ['name', 'description', 'title', 'content', 'text', 'message']

    translated_data = data.copy()

    for field in fields_to_translate:
        if field in translated_data and isinstance(translated_data[field], str):
            original_text = translated_data[field]
            translated_text = translate_text(original_text, target_lang, source_lang)
            translated_data[field] = translated_text

    return translated_data

def translate_list(items: List[Dict], target_lang: str, source_lang: str = 'en',
                   fields_to_translate: Optional[List[str]] = None) -> List[Dict]:
    """
    Translate specific fields in a list of dictionaries

    Args:
        items: List of dictionaries containing text to translate
        target_lang: Target language code
        source_lang: Source language code (default: 'en')
        fields_to_translate: List of field names to translate

    Returns:
        List of dictionaries with translated fields
    """
    if target_lang == source_lang or target_lang == 'en':
        return items

    return [translate_dict(item, target_lang, source_lang, fields_to_translate) for item in items]

def clear_translation_cache():
    """Clear the translation cache"""
    global translation_cache
    translation_cache.clear()
    logger.info("Translation cache cleared")

def get_cache_stats() -> Dict:
    """Get translation cache statistics"""
    return {
        'cache_size': len(translation_cache),
        'supported_languages': list(SUPPORTED_LANGUAGES.keys())
    }
