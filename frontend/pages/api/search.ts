// import { supabaseAdmin } from "@/utils";

export const config = {
  runtime: "edge"
};

const handler = async (req: Request): Promise<Response> => {
  try {
    const { query, apiKey, ticker } = (await req.json()) as {
      query: string;
      apiKey: string;
      ticker: string;
    };

    // const input =query;
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

    // console.log(json + "   "+ embedding)

    console.log(ticker)
    const data = await fetch("https://5000-vimarsh244-financegpt-i54aipkdx4v.ws-us92.gitpod.io/related", {
      headers: {
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        "ticker": "tatasteel",
        "ve":("["+String(embedding)+"]")
      })
    });

    const gotdata = await data.json();


    console.log("["+String(embedding)+"]")
    console.log(gotdata)

    if (!data) {
      console.error(data);
      return new Response("Error", { status: 500 });
    }

    return new Response(JSON.stringify(gotdata), { status: 200 });
  } catch (error) {
    console.error(error);
    return new Response("Error", { status: 500 });
  }
};

export default handler;
