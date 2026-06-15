import json
import robin_stocks.robinhood as rh
from ollama_robin.tools.formatter import serialize

def handle_tool_call(func_name, args, exa_client, rb_enabled):
    tool_response = ""
    
    # 1. Search Web
    if func_name == 'search_web' and exa_client:
        query = args.get('query')
        try:
            search_results = exa_client.search(
                query, type="auto", num_results=5, contents={"highlights": True}
            )
            formatted_results = []
            for idx, result in enumerate(search_results.results, 1):
                title = result.title or "Untitled"
                url = result.url
                highlight = "\n".join(result.highlights) if result.highlights else ""
                formatted_results.append(f"[{idx}] {title}\nURL: {url}\nExcerpt: {highlight}\n")
            tool_response = "\n".join(formatted_results) if formatted_results else "No results found."
        except Exception as err:
            tool_response = f"Error performing search: {err}"

    # 2. Get Accounts
    elif func_name == 'get_accounts' and rb_enabled:
        try:
            tool_response = serialize(rh.profiles.load_account_profile())
        except Exception as err:
            tool_response = f"Error: {err}"

    # 3. Get Portfolio
    elif func_name == 'get_portfolio' and rb_enabled:
        try:
            portfolio = rh.profiles.load_portfolio_profile()
            basic = rh.profiles.load_basic_profile()
            combined = {
                "equity": portfolio.get("equity"),
                "extended_hours_equity": portfolio.get("extended_hours_equity"),
                "market_value": portfolio.get("market_value"),
                "excess_margin": portfolio.get("excess_margin"),
                "buying_power": portfolio.get("buying_power"),
                "cash": portfolio.get("cash"),
                "cash_available_for_withdrawal": portfolio.get("cash_available_for_withdrawal"),
                "user_first_name": basic.get("first_name")
            }
            tool_response = serialize(combined)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 4. Get Equity Positions
    elif func_name == 'get_equity_positions' and rb_enabled:
        try:
            positions = rh.get_open_stock_positions()
            for pos in positions:
                try:
                    pos['symbol'] = rh.get_symbol_by_url(pos['instrument'])
                except:
                    pos['symbol'] = "UNKNOWN"
            tool_response = serialize(positions)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 5. Get Equity Quotes
    elif func_name == 'get_equity_quotes' and rb_enabled:
        syms = [s.strip().upper() for s in args.get('symbols', '').split(',') if s.strip()]
        try:
            quotes = rh.get_quotes(syms)
            tool_response = serialize(quotes)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 6. Get Equity Orders
    elif func_name == 'get_equity_orders' and rb_enabled:
        try:
            orders = rh.get_all_stock_orders()[:15]
            tool_response = serialize(orders)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 7. Get Equity Tradability
    elif func_name == 'get_equity_tradability' and rb_enabled:
        syms = [s.strip().upper() for s in args.get('symbols', '').split(',') if s.strip()]
        try:
            instruments = rh.get_instruments_by_symbols(syms)
            tradability = []
            for inst in instruments:
                if inst:
                    tradability.append({
                        "symbol": inst.get("symbol"),
                        "tradeable": inst.get("tradeable"),
                        "fractional_tradability": inst.get("fractional_tradability"),
                        "state": inst.get("state")
                    })
            tool_response = serialize(tradability)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 8. Review Equity Order
    elif func_name == 'review_equity_order' and rb_enabled:
        symbol = args.get('symbol').upper()
        qty = float(args.get('quantity'))
        side = args.get('side').lower()
        o_type = args.get('type').lower()
        limit_price = args.get('limit_price')
        try:
            quote = rh.get_quotes(symbol)[0]
            last_price = float(quote.get('last_trade_price', 0)) if quote else 0
            price = limit_price if o_type == 'limit' else last_price
            est_cost = price * qty
            portfolio = rh.profiles.load_portfolio_profile()
            buying_power = float(portfolio.get('buying_power', 0))
            warnings = []
            if side == 'buy' and est_cost > buying_power:
                warnings.append("WARNING: Estimated cost exceeds current buying power.")
            inst = rh.get_instruments_by_symbols(symbol)[0]
            if inst:
                if not inst.get('tradeable'):
                    warnings.append("WARNING: Asset is currently not tradeable on Robinhood.")
                if qty % 1 != 0 and not inst.get('fractional_tradability'):
                    warnings.append("WARNING: Fractional shares are not supported for this symbol.")
            else:
                warnings.append("WARNING: Ticker symbol could not be found.")

            review = {
                "symbol": symbol,
                "side": side,
                "quantity": qty,
                "price_used": price,
                "estimated_cost": est_cost,
                "available_buying_power": buying_power,
                "warnings": warnings if warnings else ["None. Order simulation looks good."]
            }
            tool_response = serialize(review)
        except Exception as err:
            tool_response = f"Error reviewing order: {err}"

    # 9. Place Equity Order
    elif func_name == 'place_equity_order' and rb_enabled:
        symbol = args.get('symbol').upper()
        qty = float(args.get('quantity'))
        side = args.get('side').lower()
        o_type = args.get('type').lower()
        limit_price = args.get('limit_price')
        try:
            if side == 'buy':
                if o_type == 'market':
                    res = rh.order_buy_market(symbol, qty)
                else:
                    res = rh.order_buy_limit(symbol, qty, limit_price)
            else:
                if o_type == 'market':
                    res = rh.order_sell_market(symbol, qty)
                else:
                    res = rh.order_sell_limit(symbol, qty, limit_price)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error placing order: {err}"

    # 10. Cancel Equity Order
    elif func_name == 'cancel_equity_order' and rb_enabled:
        oid = args.get('order_id')
        try:
            res = rh.cancel_stock_order(oid)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 11. Search Symbol
    elif func_name == 'search' and rb_enabled:
        query = args.get('query')
        try:
            res = rh.find_instrument_data(query)
            tool_response = serialize(res[:5])
        except Exception as err:
            tool_response = f"Error: {err}"

    # 12. Add to Watchlist
    elif func_name == 'add_to_watchlist' and rb_enabled:
        syms = [s.strip().upper() for s in args.get('symbols', '').split(',') if s.strip()]
        w_name = args.get('watchlist_name', 'Default')
        try:
            res = rh.post_symbols_to_watchlist(syms, w_name)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 13. Get Watchlists
    elif func_name == 'get_watchlists' and rb_enabled:
        try:
            tool_response = serialize(rh.get_all_watchlists())
        except Exception as err:
            tool_response = f"Error: {err}"

    # 14. Get Watchlist Items
    elif func_name == 'get_watchlist_items' and rb_enabled:
        w_name = args.get('watchlist_name')
        try:
            tool_response = serialize(rh.get_watchlist_by_name(w_name))
        except Exception as err:
            tool_response = f"Error: {err}"

    # 15. Unfollow / Remove from Watchlist
    elif func_name == 'unfollow_list' and rb_enabled:
        syms = [s.strip().upper() for s in args.get('symbols', '').split(',') if s.strip()]
        w_name = args.get('watchlist_name', 'Default')
        try:
            res = rh.delete_symbols_from_watchlist(syms, w_name)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 16. Get Popular Lists
    elif func_name == 'get_popular_lists' and rb_enabled:
        try:
            tool_response = serialize(rh.get_top_100()[:20])
        except Exception as err:
            tool_response = f"Error: {err}"

    # 17. Get Equity Historicals
    elif func_name == 'get_equity_historicals' and rb_enabled:
        syms = [s.strip().upper() for s in args.get('symbols', '').split(',') if s.strip()]
        interval = args.get('interval', 'day')
        span = args.get('span', 'year')
        try:
            res = rh.get_stock_historicals(inputSymbols=syms, interval=interval, span=span)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 18. Get Indexes
    elif func_name == 'get_indexes' and rb_enabled:
        tool_response = serialize([
            {"index": "S&P 500", "tracked_by_etf": "SPY", "description": "Tracks 500 largest US companies"},
            {"index": "Nasdaq 100", "tracked_by_etf": "QQQ", "description": "Tracks 100 non-financial tech giants"},
            {"index": "Dow Jones 30", "tracked_by_etf": "DIA", "description": "Tracks 30 blue-chip US giants"}
        ])

    # 19. Get Indexes Quotes
    elif func_name == 'get_indexes_quotes' and rb_enabled:
        try:
            quotes = rh.get_quotes(["SPY", "QQQ", "DIA"])
            formatted = []
            for q in quotes:
                if q:
                    formatted.append({
                        "index": "S&P 500 (SPY)" if q.get("symbol") == "SPY" else "Nasdaq-100 (QQQ)" if q.get("symbol") == "QQQ" else "Dow-30 (DIA)",
                        "price": q.get("last_trade_price"),
                        "prior_close": q.get("previous_close")
                    })
            tool_response = serialize(formatted)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 20. Get Option Chains
    elif func_name == 'get_option_chains' and rb_enabled:
        symbol = args.get('symbol').upper()
        try:
            chains = rh.get_chains(symbol)
            tool_response = serialize(chains)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 21. Get Option Instruments
    elif func_name == 'get_option_instruments' and rb_enabled:
        symbol = args.get('symbol').upper()
        exp = args.get('expiration_date')
        strike = args.get('strike_price')
        o_type = args.get('option_type')
        try:
            res = rh.find_options_by_expiration(inputSymbols=symbol, expirationDate=exp, optionType=o_type)
            if strike:
                res = [o for o in res if float(o.get('strike_price', 0)) == strike]
            tool_response = serialize(res[:10])
        except Exception as err:
            tool_response = f"Error: {err}"

    # 22. Get Option Quotes
    elif func_name == 'get_option_quotes' and rb_enabled:
        symbol = args.get('symbol').upper()
        exp = args.get('expiration_date')
        strike = float(args.get('strike_price'))
        o_type = args.get('option_type').lower()
        try:
            res = rh.get_option_market_data(symbol, exp, str(strike), o_type)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 23. Get Option Positions
    elif func_name == 'get_option_positions' and rb_enabled:
        try:
            tool_response = serialize(rh.get_open_option_positions())
        except Exception as err:
            tool_response = f"Error: {err}"

    # 24. Get Option Orders
    elif func_name == 'get_option_orders' and rb_enabled:
        try:
            tool_response = serialize(rh.get_all_option_orders()[:10])
        except Exception as err:
            tool_response = f"Error: {err}"

    # 25. Review Option Order
    elif func_name == 'review_option_order' and rb_enabled:
        symbol = args.get('symbol').upper()
        exp = args.get('expiration_date')
        strike = float(args.get('strike_price'))
        o_type = args.get('option_type').lower()
        qty = float(args.get('quantity'))
        price = float(args.get('price'))
        side = args.get('side').lower()
        try:
            market_data = rh.get_option_market_data(symbol, exp, str(strike), o_type)[0][0]
            ask = float(market_data.get('ask_price', 0))
            bid = float(market_data.get('bid_price', 0))
            est_cost = price * qty * 100
            portfolio = rh.profiles.load_portfolio_profile()
            buying_power = float(portfolio.get('buying_power', 0))
            warnings = []
            if side == 'buy' and est_cost > buying_power:
                warnings.append("WARNING: Estimated debit cost exceeds current buying power.")
            
            review = {
                "underlying": symbol,
                "option": f"{strike}{o_type[0]} exp {exp}",
                "side": side,
                "quantity": qty,
                "limit_price": price,
                "ask_price": ask,
                "bid_price": bid,
                "estimated_cost": est_cost,
                "available_buying_power": buying_power,
                "warnings": warnings if warnings else ["None. Simulation looks good."]
            }
            tool_response = serialize(review)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 26. Place Option Order
    elif func_name == 'place_option_order' and rb_enabled:
        symbol = args.get('symbol').upper()
        exp = args.get('expiration_date')
        strike = float(args.get('strike_price'))
        o_type = args.get('option_type').lower()
        qty = int(args.get('quantity'))
        price = float(args.get('price'))
        side = args.get('side').lower()
        try:
            effect = "open" if side == 'buy' else "close"
            cd = "debit" if side == 'buy' else "credit"
            res = rh.order_buy_option_limit(
                positionEffect=effect, creditOrDebit=cd, price=price, symbol=symbol,
                quantity=qty, expirationDate=exp, strike=strike, optionType=o_type
            )
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"

    # 27. Cancel Option Order
    elif func_name == 'cancel_option_order' and rb_enabled:
        oid = args.get('order_id')
        try:
            res = rh.cancel_option_order(oid)
            tool_response = serialize(res)
        except Exception as err:
            tool_response = f"Error: {err}"
            
    return tool_response
