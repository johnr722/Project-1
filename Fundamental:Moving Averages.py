def initialize(context):
    context.limit = 10
    context.max_notional = 1000000
    context.min_notional = -1000000

def before_trading_start (context):
    
    context.fundamentals = get_fundamentals(
                                            query(
                                                  
                                                  fundamentals.operation_ratios.net_income_growth,
                                                  fundamentals.earnings_ratios.diluted_eps_growth,
                                                  fundamentals.operation_ratios.revenue_growth,
                                                  fundamentals.asset_classification.growth_score,
                                                  
                                                  )
                                            .filter(
                                                    fundamentals.operation_ratios.net_income_growth > .10
                                                    )
                                            .filter(
                                                    fundamentals.operation_ratios.revenue_growth > .10
                                                    )
                                            .filter(
                                                    fundamentals.earnings_ratios.diluted_eps_growth > .10
                                                    )
                                            .order_by(
                                                      fundamentals.asset_classification.growth_score.desc()
                                                      )
                                            .limit(context.limit)
                                            )
    update_universe(context.fundamentals.columns.values)

def handle_data(context, data):
    
    cash = context.portfolio.cash
    current_positions = context.portfolio.positions
    
    for stock in data:
        
        current_position = context.portfolio.positions[stock].amount
        stock_price = data[stock].price
        
        MA1 = data[stock].mavg(10)
        MA2 = data[stock].mavg(50)
        
        invest = cash/ 10.0
        
        share_amount = int(invest)/stock_price
        
        try:
            if stock_price<invest:
                if current_position <= 0 and MA1>MA2:
                    order_target(stock, 0)
                    order(stock, int(share_amount/2))
                
                elif current_position >= 0 and MA1<MA2:
                    order_target(stock, 0)
                    order(stock, -share_amount)
    
    
    except Exception as e:
        print(str(e))





