import React, { useState } from 'react';
import type { ArticleType } from './types';

export const ArticleCard: React.FC<{ article: ArticleType }> = ({ article }) => {
  const [showMore, setShowMore] = useState(false);

  const timeString = new Date(article.date).toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' });

  return (
    <div style={{
      borderLeft: '4px solid #1E3A8A', 
      borderRadius: '4px',
      padding: '15px',
      marginBottom: '15px',
      backgroundColor: '#ffffff',
      boxShadow: '0 2px 5px rgba(0,0,0,0.05)',
      transition: 'all 0.2s ease-in-out'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <h4 style={{ margin: '0 0 10px 0', fontSize: '1.1rem', color: '#111827', lineHeight: '1.3' }}>
          {article.title}
        </h4>
        <span style={{ fontSize: '0.8rem', color: '#DC2626', fontWeight: 'bold', minWidth: '50px', textAlign: 'right' }}>
          {timeString}
        </span>
      </div>

      {showMore && (
        <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #F3F4F6', animation: 'fadeIn 0.3s' }}>
          <p style={{ fontSize: '0.9rem', color: '#4B5563', lineHeight: '1.5' }}>
            {article.description}
          </p>
          <a href={article.link} target="_blank" rel="noopener noreferrer" style={{
            display: 'inline-block',
            marginTop: '10px',
            color: '#1E3A8A',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '0.9rem'
          }}>
            Citește pe site-ul oficial ↗
          </a>
        </div>
      )}

      <button 
        onClick={() => setShowMore(!showMore)}
        style={{
          background: 'none', border: 'none',
          color: '#6B7280', cursor: 'pointer',
          fontWeight: '600', fontSize: '0.85rem',
          padding: '10px 0 0 0', width: '100%', textAlign: 'left'
        }}
      >
        {showMore ? '▲ Ascunde detaliile' : '▼ Află mai multe'}
      </button>
    </div>
  );
};