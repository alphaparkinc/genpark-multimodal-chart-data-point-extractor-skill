import sys, json
from client import MultimodalChartDataPointExtractor

def main():
    extractor = MultimodalChartDataPointExtractor()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(extractor.run_benchmark_chart_extraction(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "calibrate_axis_scale", "description": "Calibrate pixel-to-value linear mapping from axis ticks."},
                        {"name": "extract_bar_chart_series", "description": "Extract values from bar pixel coordinates."},
                        {"name": "extract_scatter_points", "description": "Extract 2D scatter coordinates."},
                        {"name": "run_benchmark_chart_extraction", "description": "Run chart coordinate extraction test suite."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "calibrate_axis_scale":
                    out = extractor.calibrate_axis_scale(args.get("tick_marks", []))
                elif tname == "extract_bar_chart_series":
                    out = extractor.extract_bar_chart_series(args.get("bars_coords", []), args.get("y_calibration", {}))
                elif tname == "extract_scatter_points":
                    out = extractor.extract_scatter_points(args.get("points_coords", []), args.get("x_calibration", {}), args.get("y_calibration", {}))
                elif tname == "run_benchmark_chart_extraction":
                    out = extractor.run_benchmark_chart_extraction()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
