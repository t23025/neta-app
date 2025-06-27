"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import axios from "axios";
import ResultTable, { Item } from "../components/ResultTable";
import { useMemo } from "react";

export default function Result() {
  const searchParams = useSearchParams();

  // 全てのパラメータ取得
  const payload = {
    query1: searchParams.get("query1"),
    query2: searchParams.get("query2"),
    startYear: searchParams.get("startYear"),
    startMonth: searchParams.get("startMonth"),
    endYear: searchParams.get("endYear"),
    endMonth: searchParams.get("endMonth"),
    durationMin: searchParams.get("durationMin") ? Number(searchParams.get("durationMin")) : undefined,
    durationMax: searchParams.get("durationMax") ? Number(searchParams.get("durationMax")) : undefined,
    dialect: searchParams.get("dialect"),
    kaga: searchParams.get("kaga")?.replace("男役", "男")?.replace("女役", "女"),
    kaya: searchParams.get("kaya")?.replace("男役", "男")?.replace("女役", "女")?.replace("ギャグ", "ギャグ")
  };

  const [data, setData] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const searchKey = useMemo(() => searchParams.toString(), [searchParams]);
  const filteredPayload = Object.fromEntries(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  Object.entries(payload).filter(([_, v]) => v !== undefined && v !== "")

  ) as typeof payload;

  useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);

      const response = await axios.post<Item[]>("http://127.0.0.1:8000/search", filteredPayload);

      setData(response.data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("検索に失敗しました。");
      }
    } finally {
      setLoading(false);
    }
  };

  fetchData();
}, [searchKey]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return <div>{data.length ? <ResultTable data={data} /> : <p>No results found.</p>}</div>;
}