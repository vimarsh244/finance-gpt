import Link from "next/link";
import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[60px] border-b border-gray-300 py-2 px-8 items-center justify-between">
      <div className="font-bold text-2xl flex items-center">
        <Link href="/">
         Finance GPT
        </Link>
      </div>
      <div>
      </div>
    </div>
  );
};
