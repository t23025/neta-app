import React from "react";//将来的な拡張を考えてリアクト


export type Item = {
  id:number;
  title:string;
  date:string;
  place:string;
  time:string;
  kaga:string;
  kaya:string;
  dialect:string;
  url:string;
  count:number;
};

interface ResultTableProps {
  data: Item[];
};

export default function ResultTable({ data }: ResultTableProps) {
  return (
    <div className="relative overflow-x-auto" >
    <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
      <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th className="px-6 py-3">ID</th>
          <th className="px-6 py-3">タイトル</th>
          <th className="px-6 py-3">投稿日</th>
          <th className="px-6 py-3">公演単独</th>
          <th className="px-6 py-3">ネタ時間</th>
          <th className="px-6 py-3">加賀</th>
          <th className="px-6 py-3">賀屋</th>
          <th className="px-6 py-3">方言</th>
          <th className="px-6 py-3">URL</th>
          <th className="px-6 py-3">再生回数</th>
        </tr>
      </thead>
      <tbody>
      {data.map((item) => (
                <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200" key={item.id}>
                  <td className="px-6 py-4">{item.id}</td>
                  <td className="px-6 py-4">{item.title}</td>
                  <td className="px-6 py-4">{item.date}</td>
                  <td className="px-6 py-4">{item.place}</td>
                  <td className="px-6 py-4">{item.time}</td>
                  <td className="px-6 py-4">{item.kaga}</td>
                  <td className="px-6 py-4">{item.kaya}</td>
                  <td className="px-6 py-4">{item.dialect}</td>
                  <td className="px-6 py-4">{item.url}</td>
                  <td className="px-6 py-4">{item.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        );
      }