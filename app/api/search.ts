import type { NextApiRequest, NextApiResponse } from 'next';
import { open } from 'sqlite';
import sqlite3 from 'sqlite3';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const db = await open({
    filename: './neta.db',
    driver: sqlite3.Database,
  });

  const keyword = (req.query.keyword as string)?.toLowerCase() ?? '';

  const query = `
    SELECT * FROM neta
    WHERE LOWER(title) LIKE ?
    OR LOWER(dialect) LIKE ?
    OR LOWER(kaga) LIKE ?
    OR LOWER(kaya) LIKE ?
  `;

  const results = await db.all(query, [
    `%${keyword}%`,
    `%${keyword}%`,
    `%${keyword}%`,
    `%${keyword}%`,
  ]);

  res.status(200).json(results);
}
