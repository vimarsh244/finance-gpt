import { IconExternalLink } from "@tabler/icons-react";
import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[60px] border-b border-gray-300 py-2 px-8 items-center justify-between">
      <div className="font-bold text-2xl flex items-center">
        <a
          className="hover:opacity-50"
          // href="https://paul-graham-gpt.vercel.app"
        >
         Finance GPT
        </a>
      </div>
      <div>
      </div>
    </div>
  );
};
