from include.repository import AlertRepository


def test_refresh_and_incident_are_deduplicated(tmp_path):
    repository = AlertRepository(f"sqlite:///{tmp_path / 'alerts.db'}")
    event = {
        "refresh_key": "refresh-1",
        "workspace_id": "workspace-1",
        "workspace_name": "Comercial",
        "dataset_id": "dataset-1",
        "dataset_name": "Vendas",
        "status": "Failed",
        "start_time": None,
        "end_time": None,
        "error_code": "GatewayNotReachable",
        "error_description": "Gateway offline",
        "payload": {},
    }

    assert repository.save_refresh(event) is True
    assert repository.save_refresh(event) is False
    assert repository.create_incident("refresh-1", "Verificar gateway") is True
    assert repository.create_incident("refresh-1", "Verificar gateway") is False
    assert repository.was_notified("refresh-1") is False

    repository.mark_notified("refresh-1")
    assert repository.was_notified("refresh-1") is True
