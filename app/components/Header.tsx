import React from "react";
import Link from "next/link";

export default function Home() {
  return (
      <header style={{ padding: '10px', background: '#eee' }}>
        <nav>
          <Link href="/">Home</Link> |{' '}
          <Link href="/profile">Profile</Link> |{' '}
          <Link href="/sns">SNS</Link>
        </nav>
      </header>
  );
}