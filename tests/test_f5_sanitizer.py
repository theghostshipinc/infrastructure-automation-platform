from python.sanitize.f5 import sanitize_lines


def test_sensitive_blocks_are_removed():
    source = [
        "cm key /Common/test.key {\n",
        '    certificate-text "-----BEGIN PRIVATE KEY-----\n',
        "    SECRET-DATA\n",
        '    -----END PRIVATE KEY-----"\n',
        "}\n",
        "ltm node /Common/web01 {\n",
        "    address 10.10.11.16\n",
        "}\n",
    ]

    sanitized, removed_blocks, redacted_values = sanitize_lines(source)

    output = "".join(sanitized)

    assert removed_blocks == 1
    assert redacted_values == 0
    assert "BEGIN PRIVATE KEY" not in output
    assert "SECRET-DATA" not in output
    assert "ltm node /Common/web01" in output


def test_password_values_are_redacted():
    source = [
        "auth user admin {\n",
        "    encrypted-password super-secret-hash\n",
        "    role admin\n",
        "}\n",
    ]

    sanitized, removed_blocks, redacted_values = sanitize_lines(source)

    output = "".join(sanitized)

    assert removed_blocks == 0
    assert redacted_values == 1
    assert "super-secret-hash" not in output
    assert "encrypted-password <REDACTED>" in output
    assert "role admin" in output


def test_certificate_block_is_removed():
    source = [
        "cm cert /Common/test.crt {\n",
        '    certificate-text "-----BEGIN CERTIFICATE-----\n',
        "    CERTIFICATE-DATA\n",
        '    -----END CERTIFICATE-----"\n',
        "}\n",
        "ltm pool /Common/app_pool {\n",
        "    load-balancing-mode round-robin\n",
        "}\n",
    ]

    sanitized, removed_blocks, redacted_values = sanitize_lines(source)

    output = "".join(sanitized)

    assert removed_blocks == 1
    assert redacted_values == 0
    assert "CERTIFICATE-DATA" not in output
    assert "ltm pool /Common/app_pool" in output


def test_normal_ltm_configuration_is_preserved():
    source = [
        "ltm virtual /Common/vs_web {\n",
        "    destination /Common/10.10.12.100:80\n",
        "    pool /Common/pool_web\n",
        "}\n",
    ]

    sanitized, removed_blocks, redacted_values = sanitize_lines(source)

    output = "".join(sanitized)

    assert removed_blocks == 0
    assert redacted_values == 0
    assert "ltm virtual /Common/vs_web" in output
    assert "destination /Common/10.10.12.100:80" in output
    assert "pool /Common/pool_web" in output