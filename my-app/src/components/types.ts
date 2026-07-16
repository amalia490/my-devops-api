import { gql, type TypedDocumentNode } from '@apollo/client';

export const GET_NEWS: TypedDocumentNode<NewsData, any> = gql`
  query GetNews {
    NewsSources {
      id
      name
      category
      Articles {
        id
        title
        description
        link
        date
      }
    }
  }
`;

export const GET_CHANNEL_DETAILS: TypedDocumentNode<ChannelDetailsData, any> = gql`
  query GetChannelDetails($NewsSourceId: Int!) {
    NewsSourcesById(NewsSourceId: $NewsSourceId) { 
      id
      name
      category
      Articles {
        id
        title
        description
        link
        date
      }
    }
  }
`;

export const SUBSCRIBE_MUTATION: TypedDocumentNode<any, SubscribeVariables> = gql`
  mutation Subscribe($email: String!, $isActive: Boolean!) {
    addSubscriber(email: $email, isActive: $isActive)
  }
`;

export interface SubscribeVariables {
  email: string;
  isActive: boolean;
}

export interface ArticleType {
  id: number;
  title: string;
  description: string;
  link: string;
  date: string;
}

export interface NewsSourceType {
  id: number;
  name: string;
  category: string;
  Articles: ArticleType[];
}

export interface ChannelDetailsData {
  NewsSourcesById: NewsSourceType; 
}

export interface NewsData{
    NewsSources: NewsSourceType[]
}