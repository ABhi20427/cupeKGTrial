import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpApi from 'i18next-http-backend';

i18n
  .use(HttpApi) // Load translations using http
  .use(LanguageDetector) // Detect user language
  .use(initReactI18next) // Pass i18n instance to react-i18next
  .init({
    supportedLngs: ['en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa'],
    fallbackLng: 'en',
    debug: false,

    // Detection options
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },

    // Backend options
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    // React options
    react: {
      useSuspense: false, // Disable suspense to avoid synchronous input errors
    },

    interpolation: {
      escapeValue: false, // React already escapes values
    },
  });

export default i18n;
