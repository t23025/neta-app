// カスタムボタンコンポーネントをインポート（デザインが事前に適用された汎用的なボタン）
import { Button } from "./button";

// Props（外部から受け取るデータ）の型定義
type AvailabilitySelectorProps = {
  options: string[]; // 選択肢（例: ["あり", "なし"] など）
  selected: string | null; // 現在選択されている値（選択されていなければ null）
  onChange: (value: string | null) => void; // 選択が変更された時に呼び出される関数
};

// 選択肢ボタンの UI を表示するコンポーネント定義
export const AvailabilitySelector = ({
  options,
  selected,
  onChange,
}: AvailabilitySelectorProps) => {
  return (
    <div className="flex gap-4">
      {options.map((option) => {
        const isSelected = selected === option;

        return (
          <Button
            key={option}
            onClick={() => onChange(isSelected ? null : option)}
            className={`w-[115px] h-[66px] rounded-[10px] border border-solid text-[32px] 
              ${isSelected ? "bg-[#ababab] text-black border-[#000000]" : "bg-[#faf6ee] text-black border-black"}`}
            variant="outline"
          >
            {option}
          </Button>
        );
      })}
    </div>
  );
};
