import React from "react";
import Kagaprofile from "../components/Kagaprofile";
import Kayaprofile from "../components/Kayaprofile";



export default function Home() { //Homeコンポーネントを定義してして外部に公開
  return (
    <>
      <h1>プロフィール</h1>
      <p style={{ fontSize: "0.8rem", color: "#666" }}>
  ※プロフィール情報は事務所公式サイトを参考にしています。<br />
  詳しいプロフィールは事務所公式サイトをご覧ください。<br />
  出典：
  <a href="https://www.maseki.co.jp/talent/kagaya" target="_blank" rel="noopener noreferrer" style={{ color: "#0070f3" }}>
    マセキ芸能社（かが屋）
  </a>
</p>


      <Kagaprofile /><br />
      <Kayaprofile />

    </>
  );
}


