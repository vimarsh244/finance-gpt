// import { supabaseAdmin } from "@/utils";

export const config = {
  runtime: "edge"
};

const handler = async (req: Request): Promise<Response> => {
  try {
    const { query, apiKey, ticker, matches } = (await req.json()) as {
      query: string;
      apiKey: string;
      matches: number;
      ticker: string;
    };

    const input = query.replace(/\n/g, " ");
    

    const res = await fetch("https://api.openai.com/v1/embeddings", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`
      },
      method: "POST",
      body: JSON.stringify({
        model: "text-embedding-ada-002",
        input
      })
    });

    const json = await res.json();
    const embedding = json.data[0].embedding;

    // const { data: chunks, error } = await supabaseAdmin.rpc("pg_search", {
    //   query_embedding: embedding,
    //   similarity_threshold: 0.01,
    //   match_count: matches
    // });

    const data = await fetch("https://deployed.render.com/related", {
      
      method: "POST",
      body: JSON.stringify({
        "ticker": ticker,
        "ev":String(embedding)
      })
    });


    // if (error) {
    //   console.error(error);
    //   return new Response("Error", { status: 500 });
    // }

    return new Response(JSON.stringify(data), { status: 200 });
  } catch (error) {
    console.error(error);
    return new Response("Error", { status: 500 });
  }
};

export default handler;
