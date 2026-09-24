(function defineMathAlreadyStructuredDataHelper() {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  function cleanText(value) {
    return (value || '').replace(/\s+/g, ' ').trim();
  }

  function firstText(selectors) {
    for (var i = 0; i < selectors.length; i++) {
      var el = document.querySelector(selectors[i]);
      if (el && el.textContent) {
        var text = cleanText(el.textContent);
        if (text) {
          return text;
        }
      }
    }
    return '';
  }

  function extractQuestionText() {
    var formParagraphs = document.querySelectorAll('form p');
    for (var i = 0; i < formParagraphs.length; i++) {
      var text = cleanText(formParagraphs[i].textContent);
      if (!text) {
        continue;
      }
      if (/^answer:?$/i.test(text)) {
        continue;
      }
      if (/^\([A-E]\)$/i.test(text)) {
        continue;
      }
      if (text.length < 15) {
        continue;
      }
      return text;
    }

    var articleParagraphs = document.querySelectorAll('.article p');
    for (var j = 0; j < articleParagraphs.length; j++) {
      var articleText = cleanText(articleParagraphs[j].textContent);
      if (articleText && !/^answer:?$/i.test(articleText) && articleText.length >= 15) {
        return articleText;
      }
    }
    return '';
  }

  function addJsonLd(schema, schemaKey) {
    if (!schema) {
      return;
    }
    var existingSelector = 'script[type="application/ld+json"][data-mathalready-schema="' + schemaKey + '"]';
    if (document.querySelector(existingSelector)) {
      return;
    }
    var script = document.createElement('script');
    script.type = 'application/ld+json';
    script.setAttribute('data-mathalready-schema', schemaKey);
    script.text = JSON.stringify(schema);
    document.head.appendChild(script);
  }

  function buildSchema() {
    var page = window.location.pathname.split('/').pop() || '';
    var pageLower = page.toLowerCase();
    var canonical = document.querySelector('link[rel="canonical"]');
    var url = canonical ? canonical.href : window.location.href;
    var title = firstText(['h1', 'h2']) || document.title;
    var descriptionMeta = document.querySelector('meta[name="description"]');
    var description = descriptionMeta ? descriptionMeta.getAttribute('content') : '';

    if (pageLower === 'amc8_test.html') {
      return {
        '@context': 'https://schema.org',
        '@type': 'Course',
        name: title || 'AMC 8 Practice Test',
        description: description || 'Free AMC 8 practice test with multiple AMC 8-style questions.',
        provider: {
          '@type': 'Organization',
          name: 'MathAlready',
          url: 'https://www.mathalready.com/'
        },
        educationalLevel: 'Middle school',
        inLanguage: 'en',
        url: url
      };
    }

    var isAmcQuestion = /^amc8_\d{4}_\d+\.html$/.test(pageLower);
    var isSatQuestion = /^sat_.*\.html$/.test(pageLower);
    if (!isAmcQuestion && !isSatQuestion) {
      return null;
    }

    var schema = {
      '@context': 'https://schema.org',
      '@type': 'Quiz',
      name: title || document.title,
      description: description || ('Practice question on ' + (isAmcQuestion ? 'AMC 8' : 'SAT Math') + '.'),
      isAccessibleForFree: true,
      inLanguage: 'en',
      educationalLevel: isAmcQuestion ? 'Middle school' : 'High school',
      about: {
        '@type': 'Thing',
        name: isAmcQuestion ? 'AMC 8 mathematics' : 'SAT math'
      },
      url: url
    };

    var questionText = extractQuestionText();
    if (questionText) {
      schema.hasPart = {
        '@type': 'Question',
        text: questionText
      };
    }
    return schema;
  }

  function emitSchema() {
    var schema = buildSchema();
    var page = (window.location.pathname.split('/').pop() || '').toLowerCase();
    var schemaType = schema && schema['@type'] ? schema['@type'] : 'none';
    addJsonLd(schema, page + ':' + schemaType);
  }

  window.mathAlreadyAddTestPageSchema = function () {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', emitSchema, { once: true });
      return;
    }
    emitSchema();
  };
})();
