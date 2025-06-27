import"./globals.css";
import Header from './components/Header';
import React from "react";
import { ReactNode } from "react";

export const metadata = {
 title:"neta App",
 description:"非公式ネタ検索サイト",
};

export default function RootLayout(
  {children}:
  {children:ReactNode}
  ){
  return (
    <html>
    <body>
    <Header/>
    {children}
    </body>
    </html>
  );
}