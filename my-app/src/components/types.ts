import { gql, type TypedDocumentNode } from '@apollo/client';

export const GET_NEWS: TypedDocumentNode<NewsData, any> = gql`
  query GetNews {
    NewsSources {
      id
      name
      category
      Articles(order: { date: DESC }) {
        id
        title
        description
        link
        date
      }
    }
  }
`;

export const GET_MAP_DATA: TypedDocumentNode<MapData, any> = gql`
  query GetMapData{
    Counties{
      id
      name
      latitude
      longitude 
      newsCount
    }
  }
`;

export const GET_CHANNEL_DETAILS: TypedDocumentNode<ChannelDetailsData, any> = gql`
  query GetChannelDetails($NewsSourceId: Int!) {
    NewsSourcesById(NewsSourceId: $NewsSourceId) { 
      id
      name
      category
      Articles(order: { date: DESC }) {
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

export interface CountiesType{
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  newsCount: number;
}

export interface ChannelDetailsData {
  NewsSourcesById: NewsSourceType; 
}

export interface NewsData{
    NewsSources: NewsSourceType[]
}

export interface MapData{
  Counties: CountiesType[]
}