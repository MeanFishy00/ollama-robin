# Declarative schemas for Exa and Robinhood tools

tools = [
    # Exa search tool
    {
        'type': 'function',
        'function': {
            'name': 'search_web',
            'description': 'Search the web using Exa to get up-to-date information, news, or answers.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': 'The search query or question to ask.',
                    },
                },
                'required': ['query'],
            },
        },
    },
    # Portfolio & Accounts
    {
        'type': 'function',
        'function': {
            'name': 'get_accounts',
            'description': 'View all your Robinhood accounts profile information.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_portfolio',
            'description': 'Get a snapshot of your portfolio including total value, buying power, and basic details.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_equity_positions',
            'description': 'View open equity (stock) positions with quantity and cost basis.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    # Equities
    {
        'type': 'function',
        'function': {
            'name': 'get_equity_quotes',
            'description': 'Get real-time equity quotes and prior close for up to 20 symbols.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbols': {
                        'type': 'string',
                        'description': 'Comma-separated tickers, e.g. "AAPL,MSFT"'
                    }
                },
                'required': ['symbols']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_equity_orders',
            'description': 'Get equity order status history.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_equity_tradability',
            'description': 'Check if a list of symbols can be traded and if they can be traded fractionally.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbols': {
                        'type': 'string',
                        'description': 'Comma-separated tickers, e.g. "AAPL,TSLA"'
                    }
                },
                'required': ['symbols']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'review_equity_order',
            'description': 'Simulate an equity order and get pre-trade warnings, estimated cost, and checks.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'The stock ticker, e.g. "AAPL"'},
                    'quantity': {'type': 'number', 'description': 'Number of shares'},
                    'side': {'type': 'string', 'enum': ['buy', 'sell'], 'description': 'Buy or sell'},
                    'type': {'type': 'string', 'enum': ['market', 'limit'], 'description': 'Order type'},
                    'limit_price': {'type': 'number', 'description': 'Limit price (required if type is limit)'}
                },
                'required': ['symbol', 'quantity', 'side', 'type']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'place_equity_order',
            'description': 'Place an actual equity order on Robinhood.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'The stock ticker, e.g. "AAPL"'},
                    'quantity': {'type': 'number', 'description': 'Number of shares'},
                    'side': {'type': 'string', 'enum': ['buy', 'sell'], 'description': 'Buy or sell'},
                    'type': {'type': 'string', 'enum': ['market', 'limit'], 'description': 'Order type'},
                    'limit_price': {'type': 'number', 'description': 'Limit price (required if type is limit)'}
                },
                'required': ['symbol', 'quantity', 'side', 'type']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cancel_equity_order',
            'description': 'Cancel an open equity order by ID.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {'type': 'string', 'description': 'The unique order ID'}
                },
                'required': ['order_id']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'search',
            'description': 'Find a company name or partial name to get its ticker symbol.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Company name or search phrase'}
                },
                'required': ['query']
            }
        }
    },
    # Watchlist
    {
        'type': 'function',
        'function': {
            'name': 'add_to_watchlist',
            'description': 'Add stock symbols to a watchlist.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbols': {'type': 'string', 'description': 'Comma-separated tickers to add'},
                    'watchlist_name': {'type': 'string', 'description': 'Watchlist name, default is "Default"'}
                },
                'required': ['symbols']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_watchlists',
            'description': 'List all watchlists on your account.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_watchlist_items',
            'description': 'List symbols inside a specific watchlist.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'watchlist_name': {'type': 'string', 'description': 'Name of the watchlist'}
                },
                'required': ['watchlist_name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'unfollow_list',
            'description': 'Remove symbols from a watchlist.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbols': {'type': 'string', 'description': 'Comma-separated tickers to remove'},
                    'watchlist_name': {'type': 'string', 'description': 'Watchlist name, default is "Default"'}
                },
                'required': ['symbols']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_popular_lists',
            'description': 'Discover popular Robinhood lists (100 most popular stocks).',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    # Market Data
    {
        'type': 'function',
        'function': {
            'name': 'get_equity_historicals',
            'description': 'Get OHLCV price bars across a time range.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbols': {'type': 'string', 'description': 'Comma-separated tickers, e.g. "AAPL,TSLA"'},
                    'interval': {'type': 'string', 'enum': ['5minute', '10minute', 'hour', 'day', 'week'], 'description': 'Interval of bars'},
                    'span': {'type': 'string', 'enum': ['day', 'week', 'month', '3month', 'year', '5year'], 'description': 'Time span'}
                },
                'required': ['symbols']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_indexes',
            'description': 'Look up market index symbols and descriptors (e.g. S&P 500, Nasdaq, Dow).',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_indexes_quotes',
            'description': 'Get real-time values of major indexes (via ETFs SPY, QQQ, DIA).',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    # Options
    {
        'type': 'function',
        'function': {
            'name': 'get_option_chains',
            'description': 'Load option chain info including available expiration dates.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'Underlying stock ticker'}
                },
                'required': ['symbol']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_option_instruments',
            'description': 'Load option contracts filtered by expiration and strike.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'Underlying stock ticker'},
                    'expiration_date': {'type': 'string', 'description': 'Expiration date (YYYY-MM-DD)'},
                    'strike_price': {'type': 'number', 'description': 'Strike price'},
                    'option_type': {'type': 'string', 'enum': ['call', 'put'], 'description': 'Call or put'}
                },
                'required': ['symbol', 'expiration_date']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_option_quotes',
            'description': 'Get real-time quotes for option contracts.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'Underlying stock ticker'},
                    'expiration_date': {'type': 'string', 'description': 'Expiration date (YYYY-MM-DD)'},
                    'strike_price': {'type': 'number', 'description': 'Strike price'},
                    'option_type': {'type': 'string', 'enum': ['call', 'put'], 'description': 'Call or put'}
                },
                'required': ['symbol', 'expiration_date', 'strike_price', 'option_type']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_option_positions',
            'description': 'View open or closed options positions.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_option_orders',
            'description': 'Get options order history.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'review_option_order',
            'description': 'Simulate an options order and get pre-trade warnings, bid/ask spreads, and buying power requirements.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'Underlying ticker'},
                    'expiration_date': {'type': 'string', 'description': 'Expiration date (YYYY-MM-DD)'},
                    'strike_price': {'type': 'number', 'description': 'Strike price'},
                    'option_type': {'type': 'string', 'enum': ['call', 'put']},
                    'quantity': {'type': 'number', 'description': 'Number of contracts'},
                    'price': {'type': 'number', 'description': 'Limit price per contract'},
                    'side': {'type': 'string', 'enum': ['buy', 'sell']}
                },
                'required': ['symbol', 'expiration_date', 'strike_price', 'option_type', 'quantity', 'price', 'side']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'place_option_order',
            'description': 'Place a real options limit order on Robinhood.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {'type': 'string', 'description': 'Underlying ticker'},
                    'expiration_date': {'type': 'string', 'description': 'Expiration date (YYYY-MM-DD)'},
                    'strike_price': {'type': 'number', 'description': 'Strike price'},
                    'option_type': {'type': 'string', 'enum': ['call', 'put']},
                    'quantity': {'type': 'number', 'description': 'Number of contracts'},
                    'price': {'type': 'number', 'description': 'Limit price per contract'},
                    'side': {'type': 'string', 'enum': ['buy', 'sell']}
                },
                'required': ['symbol', 'expiration_date', 'strike_price', 'option_type', 'quantity', 'price', 'side']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'cancel_option_order',
            'description': 'Cancel an open options order by ID.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'order_id': {'type': 'string', 'description': 'The option order ID'}
                },
                'required': ['order_id']
            }
        }
    }
]
