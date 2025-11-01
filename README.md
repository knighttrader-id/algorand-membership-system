# 🎫 Algorand Membership System

> A decentralized membership management smart contract built on Algorand blockchain using Python and ARC-4 standards.

[![Algorand](https://img.shields.io/badge/Algorand-000000?style=for-the-badge&logo=algorand&logoColor=white)](https://www.algorand.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ARC-4](https://img.shields.io/badge/ARC--4-ABI-blue?style=for-the-badge)](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0004.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📖 Project Description

The **Algorand Membership System** is a smart contract that enables decentralized membership management on the Algorand blockchain. Users can purchase memberships by paying a fixed fee, which grants them access for a predetermined duration (1000 rounds). The contract securely tracks membership status and expiration dates using Algorand's local state, ensuring transparency and immutability.

This project demonstrates best practices in Algorand smart contract development using:

- **Algopy (Puya)** - Python-based smart contract language
- **ARC-4** - Algorand's standard for Application Binary Interface (ABI)
- **AlgoKit** - Developer toolkit for Algorand

---

## ✨ What It Does

The membership system provides a simple yet powerful way to manage subscriptions or memberships on-chain:

1. **Join/Renew Membership**: Users pay 1 ALGO to become a member or renew their existing membership
2. **Track Expiration**: Each membership is valid for 1000 rounds (blocks) from the purchase time
3. **Verify Membership**: Anyone can check if an address has an active membership
4. **Query Expiration**: Get the exact round number when a membership expires

The contract uses **atomic transactions** to ensure that payment and membership activation happen simultaneously, preventing any edge cases or inconsistencies.

---

## 🚀 Features

### Core Functionality

- ✅ **Payment-Based Membership**: Pay 1 ALGO (1,000,000 microAlgos) to activate membership
- ✅ **Time-Limited Access**: Membership expires after 1000 rounds (~1000 seconds on Algorand)
- ✅ **Renewal Support**: Users can renew their membership at any time
- ✅ **On-Chain Verification**: Membership status is stored on-chain in local state
- ✅ **Public Queries**: Anyone can check membership status without transaction fees (read-only)

### Technical Features

- 🔒 **Secure Payment Handling**: Atomic transactions ensure payment and membership activation are atomic
- 📊 **Local State Storage**: Efficient on-chain storage using Algorand's local state
- 🎯 **ARC-4 Compliant**: Follows Algorand's ABI standards for easy integration
- 🔍 **Read-Only Methods**: Gas-free membership verification queries
- 🛡️ **Input Validation**: Comprehensive checks to prevent invalid transactions

---

## 🌐 Deployed Contract

### Testnet Deployment

**Application ID:** `748955387`
**Application Address:** `SEK3B3ZYGAXRJLQH3TKZKNALAN33HJRPWRMDPCKWM3A4EM2YFDG6OFAFVI`

#### Explore on Testnet Explorer:

- [AlgoExplorer Testnet](https://testnet.explorer.perawallet.app/app/748955387)
- [AlgoScan Testnet](https://testnet.algoscan.app/app/748955387)

#### View on Dappflow:

- [Dappflow Testnet](https://app.dappflow.org/explorer/application/testnet/748955387)

---

## 🏗️ Architecture

### Smart Contract Methods

#### `create_app()`

- **Purpose**: Initializes the contract upon deployment
- **Type**: Creation method
- **Parameters**: None
- **Access**: Only called during deployment

#### `join_membership(payment, member)`

- **Purpose**: Join or renew membership
- **Type**: Application call (OptIn/NoOp)
- **Parameters**:
  - `payment`: Payment transaction (must send 1 ALGO to contract)
  - `member`: Account address becoming a member
- **Requirements**:
  - Must be called in an atomic group with payment transaction
  - Payment amount must be exactly 1,000,000 microAlgos
  - Payment must be sent to the contract address

#### `is_member(member)` (Read-Only)

- **Purpose**: Check if an account has active membership
- **Type**: Read-only query
- **Parameters**: `member` - Account address to check
- **Returns**: `true` if membership is active, `false` otherwise

#### `get_expiration_round(member)` (Read-Only)

- **Purpose**: Get the expiration round for a member
- **Type**: Read-only query
- **Parameters**: `member` - Account address
- **Returns**: Expiration round number (or 0 if not a member)

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **Docker** - Required for LocalNet (optional, for local development)
- **Poetry** - Python dependency management ([Install Poetry](https://python-poetry.org/docs/#installation))
- **AlgoKit CLI 2.0.0+** - Algorand development toolkit ([Install AlgoKit](https://github.com/algorandfoundation/algokit-cli#install))

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd membership_system/projects/membership_system
```

### 2. Install Dependencies

```bash
# Install project dependencies
algokit project bootstrap all

# Or manually with Poetry
poetry install
```

### 3. Configure Environment

```bash
# Generate environment file for localnet
algokit generate env-file -a target_network localnet

# For testnet deployment, create .env.testnet
algokit generate env-file -a target_network testnet
```

### 4. Start Local Network (Optional)

```bash
# Start AlgoKit LocalNet
algokit localnet start
```

---

## 💻 Usage

### Building the Contract

```bash
# Build all contracts
algokit project run build

# Or build specific contract
cd projects/membership_system
poetry run python -m smart_contracts build membership_system
```

### Deploying to Testnet

```bash
# Deploy to testnet
algokit project deploy testnet

# Or deploy specific contract
cd projects/membership_system
poetry run python -m smart_contracts deploy membership_system
```

### Deploying to LocalNet

```bash
# Deploy to localnet
algokit project deploy localnet
```

### Interacting with the Contract

Once deployed, you can interact with the contract using the generated client:

```python
from smart_contracts.artifacts.membership_system.membership_contract_client import (
    MembershipContractClient,
)

# Initialize client
client = MembershipContractClient(
    app_id=748955387,
    algod_client=algod_client,
)

# Check membership status (read-only, no fees)
is_active = client.is_member(member_address)
print(f"Member active: {is_active.abi_return}")

# Get expiration round
expiration = client.get_expiration_round(member_address)
print(f"Expires at round: {expiration.abi_return}")
```

---

## 🧪 Testing

The project includes comprehensive testing capabilities:

```bash
# Run tests (if test suite exists)
cd projects/membership_system
poetry run pytest

# Audit TEAL code
algokit project run audit-teal
```

---

## 📚 How It Works

### Membership Flow

1. **User Opts In**: User opts into the smart contract application
2. **Payment Transaction**: User creates a payment transaction sending 1 ALGO to the contract
3. **App Call Transaction**: User calls `join_membership()` in an atomic group with payment
4. **Validation**: Contract verifies:
   - Payment amount is exactly 1 ALGO
   - Payment sender matches app caller
   - Payment is sent to contract address
5. **State Update**: Contract stores expiration round (current round + 1000) in user's local state
6. **Verification**: Anyone can query `is_member()` to check active status

### Expiration Calculation

```
Expiration Round = Current Round + 1000
```

On Algorand, each round takes approximately 1 second, so a membership lasts roughly:

- **1000 rounds ≈ 1000 seconds ≈ 16.67 minutes**

_Note: Round times can vary slightly depending on network conditions._

---

## 🔧 Technology Stack

- **[Algorand](https://www.algorand.com/)** - Layer 1 blockchain platform
- **[Algopy (Puya)](https://github.com/algorandfoundation/puya)** - Python smart contract language
- **[AlgoKit](https://github.com/algorandfoundation/algokit-cli)** - Developer toolkit
- **[AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-py)** - Python utilities
- **[Poetry](https://python-poetry.org/)** - Dependency management

---

## 📖 Learning Resources

### Algorand Development

- [Algorand Developer Portal](https://developer.algorand.org/)
- [Algorand Python (Puya) Documentation](https://github.com/algorandfoundation/puya)
- [AlgoKit Documentation](https://github.com/algorandfoundation/algokit-cli)

### Smart Contract Standards

- [ARC-4: Application Binary Interface](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0004.md)
- [ARC-22: Algorand Smart Contract ABI](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0022.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [AlgoKit](https://github.com/algorandfoundation/algokit-cli)
- Powered by [Algorand](https://www.algorand.com/)
- Smart contract development using [Puya](https://github.com/algorandfoundation/puya)

---

## 📞 Support

For questions or issues:

- Open an issue on GitHub
- Check [Algorand Developer Forums](https://forum.algorand.org/)
- Join [Algorand Discord](https://discord.gg/algorand)

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Built with ❤️ on Algorand

</div>
