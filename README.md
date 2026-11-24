# Python License Key Verification Example (Offline-Ready)

A minimal example of node-locked software licensing for Python desktop apps (PyQt, PySide, Tkinter) and CLI tools using [Keyfern](https://keyfern.com).

Every license response is signed with **Ed25519**. The client embeds only the public key, preventing local hosts-file or mock-server spoofing and enabling verified **offline leases** when enabled for your product.

---

## Prerequisites

- Python 3.10+
- A free Keyfern account ([https://keyfern.com](https://keyfern.com))
- A Product created in your Keyfern dashboard (copy `Product ID` and `Public Key`)

*Note: Offline leases are disabled by default (`lease_days = 0`). To allow offline launches after activation, set a lease duration (1–3,650 days) in your Product settings in the Keyfern dashboard.*

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/velopre/python-license-key-example.git
cd python-license-key-example
```

### 2. Install the Keyfern SDK
```bash
pip install keyfern
```

### 3. Configure environment variables
```bash
cp .env.example .env
```
Set your `KEYFERN_PRODUCT_ID` and `KEYFERN_PUBLIC_KEY` from the Keyfern dashboard.

### 4. Run the example
```bash
python main.py
```

---

## Features

- **Ed25519 Signature Verification:** Client holds only the public key; fake local servers cannot forge valid responses.
- **Node-Locking & Floating Seats:** Limit machines per license or release inactive seats automatically.
- **Machine-Locked Free Trials:** Grant one trial per hardware ID (`/v1/trial`).
- **Clock Rollback Protection:** Refuses cached verification if the system clock is moved backward.
- **Stripe Delivery:** Connect your own Stripe account to email keys automatically on checkout (0% Keyfern commission).

---

## Pricing

Keyfern charges a flat rate based on total keys created—never per API call:
- **Free:** $0/mo for 1 product and up to 50 keys (no credit card required).
- **Starter:** $10/mo for 2 products, 1,000 keys, and Stripe integration.
- Full details: [https://keyfern.com](https://keyfern.com)

---

## License

MIT
