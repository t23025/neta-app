import type { NextApiRequest, NextApiResponse } from 'next';
// Next.js の API ハンドラーの型定義をインポート（リクエスト・レスポンスの型）
import { open } from 'sqlite';
// SQLite データベースに接続するための open 関数をインポート
import sqlite3 from 'sqlite3';
// SQLite 用のドライバをインポート（Node.js で SQLite を扱うため）

// API ルートハンドラーを定義（非同期関数）
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // SQLite データベースに接続（./neta.db ファイルを開く）
  const db = await open({
    filename: './neta.db', // データベースファイルのパス
    driver: sqlite3.Database, // 使用するドライバ
  });

  // クエリパラメータから keyword を取得し、小文字化（なければ空文字）
  const keyword = (req.query.keyword as string)?.toLowerCase() ?? '';

  // SQL クエリ：title / dialect / kaga / kaya のいずれかに keyword を含むデータを検索v
  const query = `
    SELECT * FROM neta
    WHERE LOWER(title) LIKE ?
    OR LOWER(dialect) LIKE ?
    OR LOWER(kaga) LIKE ?
    OR LOWER(kaya) LIKE ?
  `;

  // プレースホルダー（?）に同じキーワードを設定（%keyword%）
  const results = await db.all(query, [
    `%${keyword}%`, // title に含まれるか
    `%${keyword}%`, // dialect に含まれるか
    `%${keyword}%`, // kaga に含まれるか
    `%${keyword}%`, // kaya に含まれるか
  ]);

  // 結果を JSON としてクライアントに返す（HTTP ステータス 200）
  res.status(200).json(results);
}
