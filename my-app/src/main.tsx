// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import React from "react";
// import * as ReactDOM from "react-dom/client";
// import './index.css'
// import App from './App.tsx'
// import { ApolloClient, HttpLink, InMemoryCache, gql } from "@apollo/client";
// import { ApolloProvider } from "@apollo/client/react";

// const client = new ApolloClient({
// link: new HttpLink({ uri: "https://flyby-router-demo.herokuapp.com/" }),
// cache: new InMemoryCache(),
// });

// client
//   .query({
//     query: gql`
//       query GetLocations {
//         locations {
//           id
//           name
//           description
//           photo
//         }
//       }
//     `,
//   })
//   .then((result) => console.log(result));

// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )

import * as ReactDOM from "react-dom/client";
import { ApolloClient, InMemoryCache } from "@apollo/client";
import { ApolloProvider } from "@apollo/client/react";
import App from "./App";
import { HttpLink } from "@apollo/client";

const client = new ApolloClient({

  link: new HttpLink({ uri: "http://localhost:8000/graphql" }),
  cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById("root")!);

root.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);
