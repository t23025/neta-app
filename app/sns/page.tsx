import React from "react";
import { FaYoutube, FaInstagram, FaXTwitter, FaLine, FaPodcast, FaTiktok } from "react-icons/fa6";

export default function Home() {
  return (
    <>
      <h1>SNS</h1>
      <div style={{ display: "flex", flexDirection: "column", gap: "20px", marginTop: "20px" }}>
        {/* 各SNSリンクセクション */}
        <div style={{ fontSize: "1rem" }}>
          かが屋のオフィシャルコントch かが屋文庫
          <a
            href="https://www.youtube.com/@kagayabunko"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="YouTube"
          >
            <FaYoutube style={{ fontSize: "2.5rem" }} color="#FF0000" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          賀屋って普段そうやって過ごしてるんだ
          <a
            href="https://www.youtube.com/@賀屋って普段そうやって過ごして"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="賀屋YouTube個チャン"
          >
            <FaYoutube style={{ fontSize: "2.5rem" }} color="#FF0000" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          加賀インスタ
          <a
            href="https://www.instagram.com/kagaya_kaga"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="加賀Instagram"
          >
            <FaInstagram style={{ fontSize: "2.5rem" }} color="#C13584" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          賀屋インスタ
          <a
            href="https://www.instagram.com/kagaya_kaya"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="賀屋Instagram"
          >
            <FaInstagram style={{ fontSize: "2.5rem" }} color="#C13584" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          加賀X（旧Twitter）
          <a
            href="https://twitter.com/kaga_kagaya"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="加賀X"
          >
            <FaXTwitter style={{ fontSize: "2.5rem" }} color="#000000" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          賀屋X（旧Twitter）
          <a
            href="https://twitter.com/kagayahirai"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="賀屋X"
          >
            <FaXTwitter style={{ fontSize: "2.5rem" }} color="#000000" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          かが屋MG X（旧Twitter）
          <a
            href="https://twitter.com/kagaya_mg"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="MG X"
          >
            <FaXTwitter style={{ fontSize: "2.5rem" }} color="#000000" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          加賀公式LINE
          <a
            href="https://line.me/R/ti/p/@141yiwyd"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LINE"
          >
            <FaLine style={{ fontSize: "2.5rem" }} color="#00C300" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          かが屋の鶴の間（Podcast）
          <a
            href="https://podcasts.apple.com/jp/podcast/かが屋の鶴の間-rccラジオ/id1675231052"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Podcast"
          >
            <FaPodcast style={{ fontSize: "2.5rem" }} color="#9146FF" />
          </a>
        </div>

        <div style={{ fontSize: "1rem" }}>
          かが屋MG TikTok
          <a
            href="https://www.tiktok.com/@kagayamg"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="TikTok"
          >
            <FaTiktok style={{ fontSize: "2.5rem" }} color="#000000" />
          </a>
        </div>
      </div>
    </>
  );
}
