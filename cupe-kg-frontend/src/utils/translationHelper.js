import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

// Cache for translations to avoid repeated API calls
const translationCache = new Map();

/**
 * Translate text using the backend API
 */
export const translateText = async (text, targetLang, sourceLang = 'en') => {
  if (!text || targetLang === 'en' || targetLang === sourceLang) {
    return text;
  }

  const cacheKey = `${sourceLang}:${targetLang}:${text.substring(0, 100)}`;

  if (translationCache.has(cacheKey)) {
    return translationCache.get(cacheKey);
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/api/translate/text`, {
      text,
      target_lang: targetLang,
      source_lang: sourceLang
    });

    const translatedText = response.data.translatedText;
    translationCache.set(cacheKey, translatedText);
    return translatedText;
  } catch (error) {
    console.error('Translation error:', error);
    return text; // Return original text on error
  }
};

/**
 * Custom hook to translate text reactively when language changes
 */
export const useTranslatedText = (text, sourceLang = 'en') => {
  const { i18n } = useTranslation();
  const [translatedText, setTranslatedText] = useState(text);
  const [isTranslating, setIsTranslating] = useState(false);

  useEffect(() => {
    const translate = async () => {
      if (!text || i18n.language === 'en') {
        setTranslatedText(text);
        return;
      }

      setIsTranslating(true);
      const translated = await translateText(text, i18n.language, sourceLang);
      setTranslatedText(translated);
      setIsTranslating(false);
    };

    translate();
  }, [text, i18n.language, sourceLang]);

  return { translatedText, isTranslating };
};

/**
 * Custom hook to translate an object with multiple fields
 */
export const useTranslatedObject = (obj, fieldsToTranslate = []) => {
  const { i18n } = useTranslation();
  const [translatedObj, setTranslatedObj] = useState(obj);
  const [isTranslating, setIsTranslating] = useState(false);

  useEffect(() => {
    const translateObject = async () => {
      if (!obj || i18n.language === 'en') {
        setTranslatedObj(obj);
        return;
      }

      setIsTranslating(true);
      const translated = { ...obj };

      for (const field of fieldsToTranslate) {
        if (obj[field] && typeof obj[field] === 'string') {
          translated[field] = await translateText(obj[field], i18n.language);
        }
      }

      setTranslatedObj(translated);
      setIsTranslating(false);
    };

    translateObject();
  }, [obj, i18n.language, fieldsToTranslate]);

  return { translatedObj, isTranslating };
};

/**
 * Translate multiple items in an array
 */
export const translateArray = async (items, fieldsToTranslate, targetLang, sourceLang = 'en') => {
  if (!items || items.length === 0 || targetLang === 'en') {
    return items;
  }

  const translatedItems = await Promise.all(
    items.map(async (item) => {
      const translated = { ...item };
      for (const field of fieldsToTranslate) {
        if (item[field] && typeof item[field] === 'string') {
          translated[field] = await translateText(item[field], targetLang, sourceLang);
        }
      }
      return translated;
    })
  );

  return translatedItems;
};
