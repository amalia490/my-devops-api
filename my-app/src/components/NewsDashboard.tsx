import type { NewsData, NewsSourceType } from './types';
import { ChannelColumn } from './ChannelColumn';

export const NewsDashboard: React.FC <NewsData> = ({ NewsSources }) => {
  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px', fontFamily: 'system-ui, sans-serif' }}>

      <main style={{ display: 'flex', gap: '25px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
        {NewsSources?.map((source: NewsSourceType) => {
          console.log("Se randează canalul:", source.name, "cu ID:", source.id);
          console.log("Articole pentru acest canal:", source.Articles);
          return <ChannelColumn key={source.id} source={source} />
        })}
      </main>
      
    </div>
  );
};