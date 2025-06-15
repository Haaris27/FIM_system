import { Card, Text } from "@tremor/react";
import { ShieldCheckIcon, ExclamationCircleIcon, TrashIcon } from "@heroicons/react/24/solid";

interface MetricCardProps {
  title: string;
  value: number;
  icon: "shield" | "alert" | "warning";
}

export function MetricCard({ title, value, icon }: MetricCardProps) {
  const IconComponent = {
    shield: ShieldCheckIcon,
    alert: ExclamationCircleIcon,
    warning: TrashIcon
  }[icon];

  return (
    <Card className="bg-purple-900/40 backdrop-blur-xl border border-violet-400/20 relative overflow-hidden group animate-glow">
      <div className="absolute inset-0 bg-gradient-to-r from-violet-600/20 via-purple-500/20 to-violet-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div className="flex items-center space-x-4">
        <IconComponent className="h-8 w-8 text-violet-300" />
        <div>
          <Text className="text-violet-200/80">{title}</Text>
          <Text className="text-3xl font-bold text-violet-100">{value}</Text>
        </div>
      </div>
    </Card>
  );
}
