import { Button } from "./button";

type AvailabilitySelectorProps = {
  options: string[]; // ["あり", "なし"] など
  selected: string | null;
  onChange: (value: string | null) => void;
};

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
