def check_honeypot(token_contract, your_wallet):
    try:
        try:
            owner = token_contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                print("✅ Ownership renounced.")
            else:
                print("❌ Ownership NOT renounced:", owner)
                return False
        except:
            print("⚠️ 'owner()' method not found — might be safe or suspicious.")
        
        try:
            token_contract.functions.balanceOf(your_wallet).call()
            print("✅ balanceOf callable.")
        except:
            print("❌ balanceOf not callable.")
            return False

        print("✅ Basic checks passed. Run dynamic test trade to confirm.")

        return True

    except Exception as e:
        print("🚫 Error during analysis:", str(e))
        return False