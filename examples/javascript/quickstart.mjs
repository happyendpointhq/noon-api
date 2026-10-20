// Noon API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs laptop ae

const HOST = 'noon7.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Noon API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const query = process.argv[2] ?? 'laptop';
const region = process.argv[3] ?? 'ae';
const results = await get('/product-search', { region, query, page_size: 5 });
console.log(`About ${results.totals.estimated_matches} matches on noon ${region}`);
for (const item of results.items) {
  console.log(`${item.currency} ${String(item.price).padStart(9)}  ${item.brand}  ${item.sku}  ${item.name.slice(0, 60)}`);
}
